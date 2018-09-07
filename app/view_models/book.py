"""
对应book数据的view_model
view_model作用:
	1.统一数据
	2.裁剪数据
	3.补充数据
"""

class BookViewModel:
	"""BookViewModel 只处理单本数据"""

	def __init__(self, book):
		self.title = book['title']
		self.publisher = book['publisher']
		self.author = ' '.join(book['author'])
		self.image = book['image']
		self.price= book['price']
		self.summary = book['summary']
		self.isbn = book['isbn']
		self.pages = book['pages']
		self.pubdate = book['pubdate']
		self.binding = book['binding']

	@property
	def intro(self):
		intros = filter(lambda x: True if x else False, [self.author, self.publisher, self.price])
		return ' / '.join(intros)

class BookCollection:
	"""包含一组 BookViewModel 处理一组书籍数据"""

	def __init__(self):
		self.total = 0
		self.books = []
		self.keyword = ''

	def fill(self, yushu_book, keyword):
		self.total = yushu_book.total
		self.keyword = keyword
		self.books = [BookViewModel(book) for book in yushu_book.books]
		


		

# 弃用 以下是练习时的伪面向对象代码
class __BookViewModel:
	"""package_single package_collection 对应鱼书API的两种数据格式"""

	# 单本
	@classmethod
	def package_single(cls, data, keyword):
		returned = {
			'books':[],
			'total':0,
			'keyword':keyword
		}
		if data:
			returned['total'] = 1	# 如果数据不为空 则total有1
			returned['books'] = [cls.__cut_book_data(data)]
		return returned

	# 集合
	@classmethod
	def package_collection(cls, data, keyword):
		returned = {
			'books':[],
			'total':0,
			'keyword':keyword
		}
		if data:
			returned['total'] = data['total']
			returned['books'] = [cls.__cut_book_data(book) for book in data['books']]
		return returned

	# 用于裁剪数据 data为原始数据
	@classmethod
	def __cut_book_data(cls, data):
		book = {
			'title':data['title'],
			'publisher':data['publisher'],
			'pages':data['pages'] or '',	# 非空则返回原来的data['pages'] 否则返回''字符串
			'author':' '.join(data['author']),
			'price':data['price'],
			'summary':data['summary'] or '',
			'image':data['image']
		}
		return book