"""
测试代码
"""

from flask import Flask, current_app

app = Flask(__name__)

# 应用上下文 对核心对象Flask的封装
# 请求上下文	对Request的封装

# Flask 存储在AppContext
# Request 存储在RequestContext
# 想操作Flask，Request 要通过上下文对象 AppContext，RequestContext

# flask有一个应用栈，一个请求栈
# 当有请求到来时，先查看应用栈是否为空或不为请求所对应的app 若为空或不为请求所对应的app则先将对应app压入应用栈 后将请求压入请求栈
# current_app实际上是指向应用栈栈顶的指针(会返回核心对象) 非上下文环境指的是应用栈为空
# 当请求结束时 两个栈的元素都会被弹出

# 此处手动入栈 
# 当编写离线应用,单元测试 则需要手动入栈
# ctx = app.app_context()
# ctx.push()
# a = current_app
# d = current_app.config['DEBUG']
# print(a,d)

# 写法二：通过with手动入栈
with app.app_context():
	a = current_app
	d = current_app.config['DEBUG']
	print(a,d)
