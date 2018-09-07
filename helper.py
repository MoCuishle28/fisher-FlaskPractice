

def is_isbn_or_key(word):
	"""
	判断是isbn还是关键字
	"""

	# isbn: isbn13 13个0-9的数字组成
	# 		isbn10 10个0-9的数字组成 含有一些'-'

	# 默认传过来的参数是关键字
	isbn_or_key = 'key'
	# q.isdigit()判断q是否全是数字
	if len(word) == 13 and word.isdigit():
		isbn_or_key = 'isbn'
	# 先判断是否有'-' 然后去掉'-'(q.replace('-',''))再判断是否全长度为10且剩下的是数字
	short_word = word.replace('-','')
	if '-' in word and len(short_word) == 10 and short_word.isdigit():
		isbn_or_key = 'isbn'
		
	return isbn_or_key