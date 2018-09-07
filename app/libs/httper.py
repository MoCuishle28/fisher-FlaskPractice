"""
负责API的http请求
"""

import requests


class HTTP:
	"""
	使用HTTP类对get方法进行封装是为了好扩展
	Class HTTP 和 Class HTTP(object) 在python3中没区别
	"""

	# 调用API的get  @staticmethod静态方法(可以去掉self)
	@staticmethod
	def get(url, return_json=True):
		r = requests.get(url)
		# 大部分API格式都是restful 会返回json

		# # 如果状态码为200 即成功返回数据
		# if r.status_code == 200:
		# 	# 如果返回的是json格式
		# 	if return_json:
		# 		# 将返回的json解析为字典
		# 		return r.json()
		# 	else:
		# 		return r.text
		# # 否则状态码不为200 即没有成功返回数据
		# else:
		# 	if return_json:
		# 		return {}
		# 	else:
		# 		return ''

		# 以上代码可以三元表达式简化
		if r.status_code != 200:
			return {} if return_json else ''
		return r.json() if return_json else r.text
