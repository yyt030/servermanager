#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'
from flask import Blueprint, render_template, flash, redirect, url_for

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
