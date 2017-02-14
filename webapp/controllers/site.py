#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'
from flask import (Blueprint, render_template, request, flash, redirect, url_for)

from webapp import db, cache
from webapp.forms.server import ServerForm
from webapp.models.server import Server, Subproject
from webapp.models.user import Permission

bp = Blueprint('site', __name__)


@bp.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


@bp.route('/login')
def login():
    return render_template('login.html')


@bp.route('/')
def index():
    return render_template('base.html')


@bp.route('/serverlist')
def serverlist():
    return redirect(url_for('s.index'))


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
