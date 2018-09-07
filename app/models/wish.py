"""心愿模型 用于心愿清单 与Gift大体相同"""

from app.models.base import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, desc, func
from sqlalchemy.orm import relationship
from app.spider.yushu_book import YuShuBook


class Wish(Base):
	id = Column(Integer, primary_key=True)
	user = relationship('User')
	uid = Column(Integer, ForeignKey('user.id'))	# Foreignkey取得是上面relationship的user 若上面改变量名，这里也要改
	isbn = Column(String(15), nullable=False)	# 通过isbn做关联
	launched = Column(Boolean, default=False)	# 是否赠送出去 默认未赠送出去

	@classmethod
	def get_user_wishes(cls, uid):
		wishes = Wish.query.filter_by(
			uid=uid, launched=False).order_by(
			desc(Wish.create_time)).all()

	@classmethod
	def get_gifts_counts(cls, isbn_list):
		# 根据传入的一组isbn 到Wish表中计算出每个礼物的Wish（心愿）数量
		# 跨表（模型） 查询要用到db.session()
		# filter接收条件表达式	func.count()用于统计数量
		count_list = db.session.query(func.count(Gift.id), 
			Gift.isbn).filter(Gift.launched == False, 
							Gift.isbn.in_(isbn_list), 	# mysql 的in查询
							Gift.status == 1).group_by(
							Gift.isbn).all()
		count_list = [{'count':w[0], 'isbn':w[1]} for w in count_list]
		return count_list	# 直接返回元组列表不好用

		# 拿到对应的书籍
	@property
	def book(self):
		yushu_book = YuShuBook()
		yushu_book.search_by_isbn(self.isbn)
		return yushu_book.first

# 防止循环导入
from app.models.gift import Gift