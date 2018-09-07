"""
应用的初始化 即核心对象app的初始化
加上__init__.py 文件夹则变为python包
"""

from flask import Flask
from flask_login import LoginManager
from app.models.book import db
from flask_mail import Mail

# isbn = 9787532736942 可用

login_manager = LoginManager()
mail = Mail()

def create_app():
	app = Flask(__name__)

	# 导入配置文件 参数->模块路径
	# 配置文件里的必须全大写,否则会被忽略(例如:Debug会被忽略)
	app.config.from_object('app.secure')
	app.config.from_object('app.setting')

	register_blueprint(app)	# 注册蓝图
	login_manager.init_app(app)	# 登录插件的初始化
	login_manager.login_view = 'web.login'	# 未授权（未登录）时跳回登录页面
	login_manager.login_messages = '请先登录'	# 未授权（未登录）时闪现的消息

	mail.init_app(app)	# 注册mail 发送邮箱的插件

	db.init_app(app) # 创建model要和核心对象app关联起来 此处关联app但没有为SQLAlchemy对象保存app(在函数内部仅作为临时变量)，因此下面完成映射时还需传入app
	db.create_all(app=app) # 将数据模型映射到数据库里 第一种写法：直接传入app引用
	# 将数据模型映射到数据库里 第二种写法：
	# with app.app_context():
	# 	db.create_all()
	# 第三种写法：在构造SQLAlchemy时将核心对象app传入(此工程在models/book.py 内创建了)
	return app

# 注册蓝图对象到核心对象app上
def register_blueprint(app):
	from app.web.book import web
	app.register_blueprint(web)