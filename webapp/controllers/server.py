#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user
from flask_login import login_required
from sqlalchemy import and_

from webapp import db, cache
from webapp.forms.server import ServerForm, EditServerForm
from webapp.models.server import Server, ServerUser
from webapp.models.user import Subproject, Permission
from webapp.utils.decorators import permission_required

bp = Blueprint('s', __name__)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.SERVER_ADD)
def add():
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

    return render_template('server_info.html', active_page='add', form=form)


@bp.route('/delete', methods=['POST'])
@login_required
@permission_required(Permission.SERVER_DELETE)
def delete():
    rowids = request.form.getlist('rowid')
    server_id = request.form.get('id')
    if rowids:
        db.session.query(Server).filter(Server.id.in_(rowids)).delete(synchronize_session='fetch')
        cache.clear()
        db.session.commit()
    if server_id:
        Server.query.filter_by(id=server_id).delete()
        cache.clear()
        db.session.commit()
    flash('删除成功')
    return redirect(url_for('site.index'))


@bp.route('/deleteuser', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.SERVER_EDIT)
def deleteuser():
    server_user_id = request.form.get('id', type=int)
    if server_user_id:
        db.session.query(ServerUser).filter(ServerUser.id == server_user_id).delete(synchronize_session='fetch')
        cache.clear()
        db.session.commit()
        flash('删除用户id{}成功'.format(server_user_id))
    return redirect(url_for('site.index'))


@bp.route('/adduser', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.SERVER_EDIT)
def adduser():
    server_id = request.form.get('serverid', type=int)
    username = request.form.get('username')
    password = request.form.get('userpasswd')

    if not username or not password:
        return '无效的用户名或密码'
    Server.query.filter(Server.id == server_id).first_or_404()
    su = ServerUser.query.filter(and_(ServerUser.username == username,
                                      ServerUser.server_id == server_id)).first()
    if su:
        su.password = password
        db.session.add(su)
        db.session.commit()
    else:
        serveruser = ServerUser(username=username, password=password, server_id=server_id)
        db.session.add(serveruser)
        db.session.commit()
    return redirect(url_for('site.index'))


@bp.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def detail(id):
    server = Server.query.get_or_404(id)
    form = EditServerForm()
    if form.validate_on_submit() and current_user.can(Permission.SERVER_EDIT):
        sbs = Subproject.query.filter(Subproject.id.in_(form.subproject_id.data)).all()
        server.subprojects = []
        for sb in sbs:
            server.subprojects.append(sb)
        server.oslevel = form.oslevel.data
        server.use = form.use.data
        server.status = form.status.data
        server.owner = form.owner.data
        server.envinfo_id = form.envinfo_id.data
        cache.clear()
        db.session.add(server)
        db.session.commit()
        flash('机器信息已更新')
        return redirect(url_for('site.index'))

    form.ip.data = server.ip
    form.subproject_id.data = server.get_subproject_id
    form.oslevel.data = server.oslevel
    form.use.data = server.use
    form.status.data = server.status
    form.owner.data = server.owner
    form.envinfo_id.data = server.envinfo_id

    return render_template('server_info.html', active_page='info',
                           server=server, form=form)


@bp.route('/term/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.SERVER_LOGIN)
def term(id):
    return redirect('http://localhost:9527')
