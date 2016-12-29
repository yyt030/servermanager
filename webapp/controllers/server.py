#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'
from flask import Blueprint, render_template, flash, redirect, url_for, request

from webapp import db
from webapp.forms.server import ServerForm
from webapp.models.server import Server, Envinfo

bp = Blueprint('s', __name__)


@bp.route('/add', methods=['GET', 'POST'])
def add():
    form = ServerForm()
    form.envinfo_id.choices = [(a.id, ' '.join([a.location, a.envname])) for a in Envinfo.query.order_by('id')]
    if form.validate_on_submit():
        res = Server.query.filter_by(ip=form.ip.data).first()
        if res:
            flash('ip:{}已存在,请确认ip输入是否正确'.format(form.ip.data))
            return redirect(url_for('.add'))

        server = Server(ip=form.ip.data, project=form.project.data, oslevel=form.oslevel.data,
                        use=form.use.data, status=form.status.data, contract_person=form.contract_person.data)
        db.session.add(server)
        db.session.commit()
        flash('添加ip成功')
        return redirect(url_for('site.index'))

    return render_template('server_info.html', active_page='add', form=form)


@bp.route('/delete', methods=['POST'])
def delete():
    rowids = request.form.getlist('rowid')
    server_id = request.form.get('id')
    if rowids:
        db.session.query(Server).filter(Server.id.in_(rowids)).delete(synchronize_session='fetch')
        db.session.commit()
    if server_id:
        Server.query.filter_by(id=server_id).delete()
        db.session.commit()
    flash('删除成功')
    return redirect(url_for('site.index'))


@bp.route('/<int:id>', methods=['GET', 'POST'])
def detail(id):
    server = Server.query.get_or_404(id)
    form = ServerForm()
    if form.validate_on_submit():
        server.ip = form.ip.data
        server.project = form.project.data
        server.oslevel = form.oslevel.data
        server.use = form.use.data
        server.status = form.status.data
        server.contract_person = form.contract_person.data
        server.envinfo_id = form.envinfo_id.data
        db.session.add(server)
        db.session.commit()
        flash('机器信息已更新')
        return redirect(url_for('site.index'))

    form.ip.data = server.ip
    form.project.data = server.project
    form.oslevel.data = server.oslevel
    form.use.data = server.use
    form.status.data = server.status
    form.contract_person.data = server.contract_person
    form.envinfo_id.data = server.envinfo_id

    return render_template('server_info.html', active_page='info', server=server, form=form)


@bp.route('/term/<int:id>', methods=['GET', 'POST'])
def term(id):
    return redirect('http://localhost:9527')
