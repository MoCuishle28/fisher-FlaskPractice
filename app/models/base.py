from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from sqlalchemy import Column, Integer, SmallInteger
from contextlib import contextmanager
from datetime import datetime

class SQLAlchemy(_SQLAlchemy):
	@contextmanager
	def auto_commit(self):	# 类似上下文管理器
		try:
			yield	# yield 就返回给 with ... as 后面的内容 然后开始执行with内部代码
			self.session.commit()
		except Exception as e:
			db.session.rollback()
			raise e

db = SQLAlchemy()

class Base(db.Model):
	__abstract__ = True		# 不用创建该表
	create_time = Column('create_time', Integer)
	status = Column(SmallInteger, default=1)	# 表示软删除 默认为1

	def __init__(self):
		self.create_time = int(datetime.now().timestamp())

	# 如果有与传入字典相同的属性 就赋值
	def set_attrs(self, attrs_dict):
		for key, value in attrs_dict.items():
			if hasattr(self, key) and key != 'id':	# id由sqlalchemy动态管理
				setattr(self, key, value)

	@property
	def create_datetime(self):
		if self.create_time:
			return datetime.fromtimestamp(self.create_time)
		else:
			return None

	def delete(self):
		self.status = 0