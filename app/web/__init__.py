"""
蓝图（blueprint） 的初始化
"""
from flask import Blueprint
from flask import render_template

# 定义蓝图变量 参数-> 名称, 蓝图所在的模块
web = Blueprint('web', __name__) # 接下来可以用web注册视图函数

@web.app_errorhandler(404)	# 属于蓝图对象web的装饰器 在监听到404异常时会执行
def not_found(e):
	# 基于AOP思想 （面向切片编程）
	return render_template('404.html'), 404

# 不导入是不会执行的
from app.web import book
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish