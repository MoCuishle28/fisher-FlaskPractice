"""
用于封装业务逻辑 为了低耦合
"""

# 用http命名会报错
from app.libs.httper import HTTP
from flask import current_app

class YuShuBook:
	# 两种类型的API地址
	isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
	keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}start={}'
	
	def __init__(self):
		self.total = 0
		self.books = []

	# 类方法 cls相当于类 self指实例
	def search_by_isbn(self, isbn):
		url = self.isbn_url.format(isbn)
		# url = YuShuBook.isbn_url.format(isbn) # 也可以
		result = HTTP.get(url) # 接收到一个字典
		self.__fill_single(result)
		
	def __fill_single(self, data):
		if data:
			self.total = 1
			self.books.append(data)

	def __fill_collection(self, data):
		self.total = data['total']
		self.books = data['books']

	def search_by_keyword(self, keyword, page=1):
		# 读取配置要用到current_app(flask提供)
		url = self.keyword_url.format(keyword, current_app.config['PER_PAGE'], self.calculate_start(page))
		result = HTTP.get(url)
		self.__fill_collection(result)

	def calculate_start(self, page):
		return (page-1) * current_app.config['PER_PAGE']

	@property
	def first(self):
		return self.books[0] if self.total >= 1 else None