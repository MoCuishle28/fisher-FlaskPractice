from app import mail
from flask_mail import Message
from flask import current_app, render_template

# 异步发送
def send_async_email(app, msg):
	with app.app_contex():	# 邮件要在上下文环境中发送 所以要手动入栈
		try:
			mail.send(msg)
		except Exception as e:
			pass

def send_email(to, subject, template, **kwargs):
	"""
		to: 发给谁
		subject: 标题
		template: 内容
	"""
	msg = Message('[鱼书] '+subject ,sender=current_app.config['MAIL_USERNAME'], recipients=[to])	# recipients接收人列表
	msg.html = render_template(template, **kwargs)
	app = current_app._get_current_object()	# 从代理对象current_app中拿到真实的核心对象app 若不传入app 则在新线程中因为线程隔离 current_app在新线程中为空
	thr = Thread(target=send_async_email, args=[app, msg])	# msg是异步函数的参数
	thr.start()	# 异步发送邮箱
	
