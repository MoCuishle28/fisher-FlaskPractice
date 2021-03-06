"""
MVC 中的Model层的模型
不仅数据 业务逻辑也应该在M层
"""

from sqlalchemy import Column, Integer, String
from app.models.base import db

class Book(db.Model):
	id = Column(Integer, primary_key=True, autoincrement=True)
	title = Column(String(50), nullable=False)	# 最大长度50
	author = Column(String(30), default='未名')
	binding = Column(String(20))	# 精装还是平装
	publisher = Column(String(50))
	price = Column(String(20))
	pages = Column(Integer)
	pubdate = Column(String(20))
	isbn = Column(String(15), nullable=False, unique=True)
	summary = Column(String(1000))
	image = Column(String(50))

	
	def sample(self):
		pass