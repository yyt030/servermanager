#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'
from flask import Blueprint, render_template, flash, redirect, url_for, request

from webapp import db
from webapp.forms.server import ServerForm
from webapp.models.server import Server

bp = Blueprint('s', __name__)


@bp.route('/add', methods=['GET', 'POST'])
def add():
    form = ServerForm()
    if form.validate_on_submit():
        res = Server.query.filter_by(ip=form.ip.data).first()
        if res:
            flash('ip:{}已存在,请确认ip输入是否正确'.format(form.ip.data))
            return redirect(url_for('.add'))

        server = Server(ip=form.ip.data, project=form.project.data, oslevel=form.oslevel.data,
                        use=form.use.data, status=form.status.data)
        db.session.add(server)
        return redirect(url_for('site.index'))

    return render_template('server_add.html', active_page='add', form=form)


@bp.route('/delete', methods=['POST'])
def delete():
    rowids = request.form.getlist('rowid')
    server_id = request.form.get('id')
    if rowids:
        db.session.query(Server).filter(Server.id.in_(rowids)).delete(synchronize_session='fetch')
        db.session.commit()

    if server_id:
        print('==' * 10)
        Server.query.filter_by(id=server_id).delete()
        db.session.commit()
    return redirect(url_for('site.index'))
