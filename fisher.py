"""
入口文件 作为启动
"""

# from flask import Flask
from app import create_app

# 创建核心对象
app = create_app()

# # 以下为学习时写
# @app.route('/hello/')
# def hello():
# 	# 还有基于类的视图（即插视图）

# 	# 视图函数的返回：
# 	# status code 如：200 404 301
# 	# content-type 放在 http 的headers属性中 告诉接收方（如：浏览器）如何解析返回内容
# 	# 以上为主要内容 还有其他... 全部被封装成Response对象
# 	# return '<html>hello</html>'

# 	# 直接返回Response对象
# 	# 创建Response对象 参数-> 内容, 状态码(状态码不会对返回内容产生本质影响，该显示什么还是显示什么)
# 	# response = make_response('<html></html>', 301)

# 	# 可以修改headers
# 	headers = {
# 		# content-type 默认为 text/html
# 		# 若是以json方式解析 则改为 'application/json'
# 		# 以下改为以普通文本解析
# 		'content-type': 'text/plain'

# 		# 可以重定向
# 		# 'locaton' : 'http://www.bing.com'
# 	}

# 	# response.headers = headers
# 	# return response

# 	# 方便写法：可以让返回自动创建Response
# 	# 相当于将以下元组创建成Response后返回
# 	return '<html></html>', 301, headers

# 若不使用装饰器 @app.route() 也可使用以下方式注册
# app.add_url_rule('/hello', view_func=hello)

# if判断内语句只在作为入口文件执行
if __name__ == '__main__':
	# 生产环境下 nginx + uwsgi 有uwsgi加载flask模块执行
	# 若无 if __name__ == '__main__'...

	# host = '0.0.0.0' 表示可以接受外网访问
	# debug = True 可以不用重新编译代码 可以在网页上看到详细错误信息 但是上线前要写一个配置文件config
	# threaded=True 开启多线程模式
	app.run(host='0.0.0.0', debug=app.config['DEBUG'], threaded=True)