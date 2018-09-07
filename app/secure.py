"""
app的配置文件
机密信息 如：数据库密码等 放在这个配置文件
区别开发环境和生产环境的 如：DEBUG等
"""

DEBUG = True

# 配置数据库连接
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:zhang4409211@localhost:3306/fisher'
SECRET_KEY = '\x88D\xf09\x91\x07\x98\x89\x87\x96\xa0A\xc68\xf9\xecJ:U\x17\xc5V\xbe\x8b\xef\xd7\xd8\xd3\xe6\x98*4'

# Email 配置
MAIL_SERVER = 'smtp.qq.com'	# 电子邮箱服务器
MAIL_PORT = 465				# qq的端口
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = '476779440@qq.com'	# 自己的qq邮箱地址
MAIL_PASSWORD = 'upbkphhrpyyxcaji'		# qq邮箱授权码