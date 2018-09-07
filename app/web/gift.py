from app.libs.enums import PendingStatus
from app.models.drift import Drift
from flask import render_template, flash, request, redirect, url_for, current_app
from flask_login import login_required, current_user
from sqlalchemy import desc, func

from . import web
from app.spider.yushu_book import YuShuBook
from app.view_models.gift import MyGifts
# from app.service.gift import GiftService

from app.models import db
from app.models.gift import Gift

__author__ = '七月'


@web.route('/my/gifts') # 我还没赠送的清单
@login_required     # 必须要登录才能访问的视图函数
def my_gifts():
    uid = current_user.id
    gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
        desc(Gift.create_time)).all()
    gifts_of_mine = Gift.get_user_gifts(uid)
    isbn_list = [gift.isbn for gift in gifts]
    wish_count_list = Gift.get_wish_counts(isbn_list)
    view_model = MyGifts(gifts_of_mine, wish_count_list)
    return render_template('my_gifts.html', gifts=view_model.gifts)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):    # 赠送此书
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)

    # current_user 就是指向当前的User对象 由flask_login提供
    if current_user.can_save_to_list(isbn): # 既不在赠送清单，也不在心愿清单才能添加
        with db.auto_commit():  # 保证用户和Gift的数据都提交到数据库 保证数据一致性 还要回滚(rollback)
            # 以下代码在try内运行
            gift = Gift()
            gift.uid = current_user.id
            gift.isbn = isbn
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
    else:
        flash('这本书已添加至你的赠送清单或已存在于你的心愿清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    if not gift:
        flash('该书籍不存在，或已经交易，删除失败')
    drift = Drift.query.filter_by(gift_id=gid, pending=PendingStatus.waiting).first()
    if drift:
        flash('这个礼物正处于交易状态，请先前往鱼漂完成该交易')
    else:
        with db.auto_commit():
            current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
            gift.delete()
    return redirect(url_for('web.my_gifts'))
