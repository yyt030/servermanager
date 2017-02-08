#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'
from flask import (Blueprint, render_template, request, current_app, jsonify, flash, redirect, url_for)

from webapp import db, cache
from webapp.forms.server import ServerForm
from webapp.models.server import Server, Subproject

bp = Blueprint('site', __name__)


@bp.route('/login')
def login():
    return render_template('login.html')


@bp.route('/')
def index():
    return render_template('base.html')


@bp.route('/serverlist')
def serverlist():
    return render_template('serverlist.html')


@bp.route('/api/serverlist')
def serverlist_api():
    draw = request.args.get('draw', 1, type=int)
    start = request.args.get('start', 0, type=int)
    length = request.args.get('length', current_app.config['FLASKY_POSTS_PER_PAGE'], type=int)
    search_value = request.args.get('search[value]')

    if search_value:
        pass

    query = Server.query.order_by(Server.envinfo_id)
    pagination = query.paginate((start / length), per_page=length, error_out=False)

    servers = pagination.items
    record_total = query.count()
    result = {
        "draw": request.args.get('draw', 1, type=int),
        "recordsTotal": record_total,
        "recordsFiltered": record_total,
        "data": [
            [server.get_subproject_name, server.envinfo.location + server.envinfo.envname, server.ip, server.oslevel,
             server.contract_person] for server in servers]
    }
    return jsonify(result)


@bp.route('/serveradd')
def serveradd():
    form = ServerForm()
    if request.method == 'POST' and form.validate_on_submit():
        server = Server(ip=form.ip.data, oslevel=form.oslevel.data,
                        use=form.use.data, status=form.status.data, contract_person=form.contract_person.data)
        sbs = Subproject.query.filter(Subproject.id.in_(form.subproject_id.data)).all()
        for sb in sbs:
            server.subprojects.append(sb)
        db.session.add(server)
        db.session.commit()
        cache.clear()
        flash('ip:{}添加成功'.format(form.ip.data))
        return redirect(url_for('s.detail', id=server.id))

    return render_template('serveradd.html', form=form)
