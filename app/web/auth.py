from flask import render_template, redirect, current_app, g
from flask import request, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from flask_sqlalchemy import get_debug_queries

from . import web
from app.forms.auth import RegisterForm, LoginForm, ResetPasswordForm, EmailForm, \
    ChangePasswordForm
from app.models.user import User
from app.models import db
from app.libs.email import send_email

__author__ = '七月'


# GET是显示该页面(默认) POST是(填写后)提交
@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        user.set_attrs(form.data)
        # 以下为将用户注册信息添加到数据库
        db.session.add(user)
        db.session.commit()
        # token = user.generate_confirmation_token()
        # send_email(user.email, 'Confirm Your Account',
        #            'email/confirm', user=user, token=token)
        login_user(user, False)
        # flash('一封激活邮件已发送至您的邮箱，请快完成验证', 'confirm')
        # 由于发送的是ajax请求，所以redirect是无效的
        # return render_template('index.html')
        # return redirect(url_for('web.index'))   # 跳转到登录页面
        return redirect(url_for('web.login'))   # 跳转到登录页面
    return render_template('auth/register.html', form=form)

# GET and POST都用这个视图函数处理 所以内部有分支判断
@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):    # 判断密码是否匹配
            login_user(user, remember=True)     # 通过该函数间接将“票据”写入cookie中 remember->是否在一段时间内记住cookie
            next = request.args.get('next')     # 跳回next=的地址 即MyGift的地址
            if not next or not next.startswith('/'):    # and 后面的为了防止非法重定向
                next = url_for('web.index')
            return redirect(next)   
        else:
            flash('账号不存在或密码错误', category='login_error')
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            account_email = form.email.data
            user = User.query.filter_by(email=account_email).first_or_404()
            send_email(form.email.data, '重置你的密码',
                       'email/reset_password', user=user,
                       token=user.generate_token())
            flash('一封邮件已发送到邮箱' + account_email + '，请及时查收')
            return redirect(url_for('web.login'))
    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('web.index'))
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(token, form.password1.data)
        if success:
            flash('你的密码已更新,请使用新密码登录')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败')
            return redirect(url_for('web.index'))
    return render_template('auth/forget_password.html')


@web.route('/change/password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        current_user.password = form.new_password1.data
        db.session.commit()
        flash('密码已更新成功')
        return redirect(url_for('web.personal'))
    return render_template('auth/change_password.html', form=form)


@web.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('web.index'))


@web.route('/register/confirm/<token>')
def confirm(token):
    pass
    # if current_user.confirmed:
    #     return redirect(url_for('main.index'))
    # if current_user.confirm(token):
    #     db.session.commit()
    #     flash('You have confirmed your account. Thanks!')
    # else:
    #     flash('The confirmation link is invalid or has expired.')
    # return redirect(url_for('main.index'))


@web.route('/register/ajax', methods=['GET', 'POST'])
def register_ajax():
    if request.method == 'GET':
        return render_template('auth/register.html')
    else:
        form = RegisterForm()
        form.validate()
        user = User(form.nickname.data,
                    form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        # token = user.generate_confirmation_token()
        # send_email(user.email, 'Confirm Your Account',
        #            'email/confirm', user=user, token=token)
        login_user(user, False)
        g.status = True
        flash('一封激活邮件已发送至您的邮箱，请快完成验证', 'confirm')
        # 由于发送的是ajax请求，所以redirect是无效的
        return 'go to index'


