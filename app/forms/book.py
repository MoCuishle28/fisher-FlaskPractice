"""
验证层下的验证模块
"""
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired, Regexp
from .base import DataRequired

class SearchForm(Form):
	# q参数校验 传入的参数validators为列表，表示可以有多个校验标准（如：Length()校验长度）
	q = StringField(validators=[DataRequired(),Length(min=1, max=30)])
	# default 为默认值
	page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)

class DriftForm(Form):
	recipient_name = StringField('收件人姓名', validators=[DataRequired(), Length(min=2, max=20,
												message='收件人姓名长度必须在2到20个字符之间')])
	mobile = StringField('手机号', 
		validators=[DataRequired(),Regexp('^1[0-9]{10}$', 0, '请输入正确的手机号')])
	message = StringField('留言')
	address = StringField('邮寄地址', validators=[DataRequired(),
		Length(min=10, max=70, message='地址还不到10个字吗？尽量写详细一些吧')])