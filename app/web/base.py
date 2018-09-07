from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, SmallInteger

db = SQLAlchemy()

class Base(db.Model):
	create_time = Column('create_time', Integer)
	status = Column(SmallInteger, default=1)	# 用于软删除