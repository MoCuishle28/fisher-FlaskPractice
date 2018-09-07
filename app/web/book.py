"""
负责书籍类的业务逻辑
要将视图函数分门别类
"""
import json
from flask import jsonify  # import json
from flask import request, current_app, url_for, render_template, flash
from flask_login import current_user

from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from . import web
from app.view_models.book import BookViewModel, BookCollection
# from app.view_models.trade import TradeInfo
from app.models.gift import Gift
from app.models.wish import Wish

# 通过API做搜索
@web.route('/book/search/')
def search():
	"""
	设计url以 ?q=金庸&page=1 的方式
	q : 即能表示普通关键字 也能表示isbn
	page : 页码
	"""
	# a = request.args.to_dict() # 转为可变字典
	# 用flask提供的request提取参数 request必须由视图函数触发
	# q = request.args['q']
	# page = request.args['page']

	# q和page 要通过 验证层 验证
	form = SearchForm(request.args)
	books = BookCollection()

	if form.validate():
		q = form.q.data.strip()  # strip()去掉字符串头尾空格
		page = form.page.data
		isbn_or_key = is_isbn_or_key(q)
		yushu_book = YuShuBook()

		if isbn_or_key == 'isbn':
			yushu_book.search_by_isbn(q)
			# 弃用代码
			# result = YuShuBook.search_by_isbn(q)
			# result = BookViewModel.package_single(result, q)	# 得到原始数据后 用对应的view_models处理
		else:
			yushu_book.search_by_keyword(q, page)
			# 弃用代码
			# result = YuShuBook.search_by_keyword(q, page)
			# result = BookViewModel.package_collection(result, q)	# 得到原始数据后 用对应的view_models处理

		books.fill(yushu_book, q)
		# 以下弃用 使用原装的 需要 import json
		# return json.dumps(result), 200, {'content-type':'application/json'}
		# return jsonify(result)	# 也可以使用flask自带的 弃用

		# return jsonify(books) # python不能直接序列化对象 能序列化对象对应的字典
		# return json.dumps(books, default=lambda o: o.__dict__)	# python不能直接序列化对象 能序列化对象对应的字典
	else:
		# return jsonify(form.errors)
		flash('搜索关键字不符合要求，请重新输入关键字')
	return render_template('search_result.html', books = books)

@web.route('/book/<isbn>/detail')
# @cache.cached(timeout=1800)
def book_detail(isbn):
	"""
		1. 当书籍既不在心愿清单也不在礼物清单时，显示礼物清单
		2. 当书籍在心愿清单时，显示礼物清单
		3. 当书籍在礼物清单时，显示心愿清单
		4. 一本书要防止即在礼物清单，又在赠送清单，这种情况是不符合逻辑的

		这个视图函数不可以直接用cache缓存，因为不同的用户看到的视图不一样
		优化是一个逐步迭代的过程，建议在优化的初期，只缓存那些和用户无关的“公共数据"
	"""
	has_in_gifts = False
	has_in_wishes = False
	# isbn_or_key = is_isbn_or_key(isbn)
	# if isbn_or_key == 'isbn':
	# 获取图书信息
	yushu_book = YuShuBook()
	yushu_book.search_by_isbn(isbn)

	if current_user.is_authenticated:
		# 如果未登录，current_user将是一个匿名用户对象
		if Gift.query.filter_by(uid=current_user.id, isbn=isbn,launched=False).first():
			has_in_gifts = True
		if Wish.query.filter_by(uid=current_user.id, isbn=isbn,launched=False).first():
			has_in_wishes = True

	book = BookViewModel(yushu_book.first)
	# if has_in_gifts:
	trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()
	trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
	trade_wishes_model = TradeInfo(trade_wishes)
	trade_gifts_model = TradeInfo(trade_gifts)
	return render_template('book_detail.html', book=book, has_in_gifts=has_in_gifts,
		has_in_wishes=has_in_wishes,
		wishes=trade_wishes_model,
		gifts=trade_gifts_model)




# 学习时写的
@web.route('/test')
def test():
	r = {
		'name':'',
		'age':18
	}
	# 消息闪现
	flash('hello MoCuishle')
	return render_template('test.html', data=r)