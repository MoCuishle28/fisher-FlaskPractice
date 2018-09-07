from app.models.base import Base
from app.spider.yushu_book import YuShuBook
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, desc, func
from sqlalchemy.orm import relationship
from flask import current_app
from collections import namedtuple
from app.models import db

EachGiftWishCount = namedtuple('EachGiftWishCount', ['count', 'isbn'])	# 用namedtuple 快速定义对象 参数->名字，属性

class Gift(Base):
	id = Column(Integer, primary_key=True)
	user = relationship('User')
	uid = Column(Integer, ForeignKey('user.id'))	# Foreignkey取得是上面relationship的user 若上面改变量名，这里也要改

	# 本项目的书本数据还没存入数据库 不用这种方式做关联
	# book = relationship('Book')
	# bid = Column(Integer, ForeignKey('book.id'))
	isbn = Column(String(15), nullable=False)	# 通过isbn做关联

	launched = Column(Boolean, default=False)	# 是否赠送出去 默认未赠送出去

	def is_yourself_gift(self, uid):
		return True if self.uid == uid else False

	@classmethod
	def get_user_gifts(cls, uid):
		gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
			desc(Gift.create_time)).all()
		return gifts

	@classmethod
	def get_wish_counts(cls, isbn_list):
		# 根据传入的一组isbn 到Wish表中计算出每个礼物的Wish（心愿）数量
		# 跨表（模型） 查询要用到db.session()
		# filter接收条件表达式	func.count()用于统计数量
		count_list = db.session.query(func.count(Wish.id), 
			Wish.isbn).filter(Wish.launched == False, 
							Wish.isbn.in_(isbn_list), 	# mysql 的in查询
							Wish.status == 1).group_by(
							Wish.isbn).all()
		count_list = [{'count':w[0], 'isbn':w[1]} for w in count_list]
		return count_list	# 直接返回元组列表不好用

	# 拿到对应的书籍
	@property
	def book(self):
		yushu_book = YuShuBook()
		yushu_book.search_by_isbn(self.isbn)
		return yushu_book.first

	# 对象代表一个礼物 如果有能取多个礼物的方法则不合适
	@classmethod
	def recent(self):
		recent_gift = Gift.query.filter_by(
			launched=False).group_by(	# group_by()分组
			Gift.isbn).order_by(		# order_by()排序 desc帮助倒序排序
			desc(Gift.create_time) ).limit(	# 限制查出的条数
			current_app.config['RECENT_BOOK_COUNT']).distinct().all()	# .all()是触发语句 .first()也是 只有到了触发语句才会开始查询
		return recent_gift

# 防止循环导入 也可以在哪里用到就在哪里导入
from app.models.wish import Wish