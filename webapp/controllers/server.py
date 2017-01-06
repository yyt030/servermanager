#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'
from flask import Blueprint, render_template, flash, redirect, url_for, request
from sqlalchemy import and_

from webapp import db, cache
from webapp.forms.server import ServerForm, EditServerForm
from webapp.models.server import Server, Envinfo, ServerUser

bp = Blueprint('s', __name__)


@bp.route('/add', methods=['GET', 'POST'])
def add():
    form = ServerForm()
    form.envinfo_id.choices = [(a.id, ' '.join([a.location, a.envname])) for a in Envinfo.query.order_by('id')]
    if request.method == 'POST' and form.validate_on_submit():
        server = Server(ip=form.ip.data, subproject_id=form.subproject_id.data, oslevel=form.oslevel.data,
                        use=form.use.data, status=form.status.data, contract_person=form.contract_person.data)
        db.session.add(server)
        db.session.commit()
        cache.clear()
        flash('ip:{}添加成功'.format(form.ip.data))
        return redirect(url_for('s.detail',id=server.id))

    return render_template('server_info.html', active_page='add', form=form)


@bp.route('/delete', methods=['POST'])
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
def deleteuser():
    server_user_id = request.form.get('id', type=int)
    if server_user_id:
        db.session.query(ServerUser).filter(ServerUser.id == server_user_id).delete(synchronize_session='fetch')
        cache.clear()
        db.session.commit()
        flash('删除用户id{}成功'.format(server_user_id))
    return redirect(url_for('site.index'))


@bp.route('/adduser', methods=['GET', 'POST'])
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
def detail(id):
    server = Server.query.get_or_404(id)
    form = EditServerForm()
    if form.validate_on_submit():
        server.subproject_id = form.subproject_id.data
        server.oslevel = form.oslevel.data
        server.use = form.use.data
        server.status = form.status.data
        server.contract_person = form.contract_person.data
        server.envinfo_id = form.envinfo_id.data
        cache.clear()
        db.session.add(server)
        db.session.commit()
        flash('机器信息已更新')
        return redirect(url_for('site.index'))

    form.ip.data = server.ip
    form.subproject_id.data = server.subproject_id
    form.oslevel.data = server.oslevel
    form.use.data = server.use
    form.status.data = server.status
    form.contract_person.data = server.contract_person
    form.envinfo_id.data = server.envinfo_id

    return render_template('server_info.html', active_page='info',
                           server=server, form=form)


@bp.route('/term/<int:id>', methods=['GET', 'POST'])
def term(id):
    return redirect('http://localhost:9527')
