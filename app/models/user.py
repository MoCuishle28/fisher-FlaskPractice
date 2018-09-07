from app.models.base import Base, db
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from app.models.drift import Drift
from app.libs.enums import PendingStatus

from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager
from math import floor

class User(UserMixin, Base):
	# __tablename__ = 'user1'	# 给表重命名的属性
	id = Column(Integer, primary_key=True)
	nickname = Column(String(24), nullable=False)
	phone_number = Column(String(18), unique=True, nullable=True)
	email = Column(String(50), unique=True, nullable=False)
	confirmed = Column(Boolean, default=False)
	beans = Column(Float, default=0)	# 鱼豆
	send_counter = Column(Integer, default=0)
	receive_counter = Column(Integer, default=0)
    # 用于微信小程序
    # wx_open_id = Column(String(50))
    # wx_name = Column(String(32))
	_password = Column('password', String(100), nullable=False)		# 传入的字符串'password'是在数据库中字段的名字 若不传入则默认为变量名字

    # 属性的getter
	@property
	def password(self):
		return self._password

	@password.setter
	def password(self, raw):
		"""raw 原始密码"""
		self._password = generate_password_hash(raw)

	def check_password(self, raw):
		return check_password_hash(self._password, raw)

	# 函数名固定(在flask-login插件中) 让login_user能找到用户信息的id号 从而写入cookie 继承UserMixim就不需要写(但必须要id表示用户身份)
	# def get_id(self):
	# 	return self.id

	def can_send_drift(self):
		if self.beans < 1:
			return False
		success_gifts_count = Gift.query.filter_by(
			uid=self.id, launched=True).count()		# count 得到查询记录总数
		success_receive_count = Drift.query.filter_by(
			requester_id=self.id, pending=PendingStatus.Success).count()
		return True if floor(success_receive_count / 2) <= floor(success_gifts_count) else False	# floor 向下取整?

	def can_satisfied_wish(self, current_gift_id = None):
		if current_gift_id:
			gift = Gift.query.get(current_gift_id)
			if gift.uid == self.id:
				return False
		if self.beans < 1:
			return False
		success_gifts = Drift.query.filter(Drift.pending == PendingStatus.success,Gift.uid == self.id).count()
		success_receive = Drift.query.filter(Drift.pending == PendingStatus.success,Drift.requester_id == self.id).count()
		return False if success_gifts <= success_receive-2 else True

	def can_save_to_list(self,isbn):
		if is_isbn_or_key(isbn) != 'isbn':	# 判断是否符合isbn格式
			return False
		yushu_book = YuShuBook()
		yushu_book.search_by_isbn(isbn)		# 判断此书是否存在
		if not yushu_book.first:
			return False
		# 不允许一个用户同时赠送多本相同的书
		# 一个用户不可能同时成为此书的赠送者和索要者
		# 即 此书既不在赠送清单 也不再心愿清单 才能添加
		gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
		wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()

		if not gifting and not wishing:
			return True
		else:
			return False

	def generate_token(self, expiration=600):
		s = Serializer(current_app.config('SECRET_KEY'), expiration)	# 序列化器
		return s.dumps({'id':self.id}).decode('utf-8')
		

	@staticmethod
	def reset_password(token ,new_passord):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token.encode('utf-8'))
		except:
			return False
		uid = data.get('id')
		with db.auto_commit():
			user = User.query.get(uid)
			user.password = new_passord
		return True

	@property
	def summary(self):
		return dict(
			nickname=self.nickname,
			beans=self.beans,
			email=self.email,
			send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
		)

@login_manager.user_loader	# 让login插件使用 在试图函数中能用@login_required装饰器
def get_user(uid):
	return User.query.get(int(uid))