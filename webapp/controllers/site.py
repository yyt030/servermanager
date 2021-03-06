#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'
from flask import (Blueprint, render_template, request, flash, redirect, url_for)
from flask_login import login_user, login_required, logout_user

from webapp import db, cache
from webapp.forms.server import ServerForm
from webapp.forms.user import LoginForm
from webapp.models.server import Server, Subproject
from webapp.models.user import Permission, User
from webapp.utils.make_cache import make_cache_key

bp = Blueprint('site', __name__)


@bp.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


@bp.route('/')
@login_required
def index():
    return redirect(url_for('.dashboard'))


@bp.route('/dashboard')
def dashboard():
    return render_template('serverdashboard.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter(User.username == loginform.username.data).first()
        if user is not None and user.verify_password(loginform.password.data):
            login_user(user, loginform.remember_me.data)
            cache.clear()
            return redirect(url_for('.index'))
        flash('无效的用户名或密码')
    return render_template('login.html', loginform=loginform)


@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    cache.clear()
    return redirect(url_for('.index'))


@bp.route('/serverlist')
@cache.cached(key_prefix=make_cache_key)
def serverlist():
    return redirect(url_for('servers.index'))


@bp.route('/serveradd')
def serveradd():
    form = ServerForm()
    if request.method == 'POST' and form.validate_on_submit():
        server = Server(ip=form.ip.data, oslevel=form.oslevel.data,
                        use=form.use.data, status=form.status.data, owner=form.owner.data)
        sbs = Subproject.query.filter(Subproject.id.in_(form.subproject_id.data)).all()
        for sb in sbs:
            server.subprojects.append(sb)
        db.session.add(server)
        db.session.commit()
        cache.clear()
        flash('ip:{}添加成功'.format(form.ip.data))
        return redirect(url_for('s.detail', id=server.id))

    return render_template('serveradd.html', form=form)
