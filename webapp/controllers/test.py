#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'
from flask import Blueprint, render_template, request, current_app, jsonify

from webapp.models.server import Server

bp = Blueprint('test', __name__)


@bp.route('/login')
def login():
    return render_template('test/login.html')


@bp.route('/')
def index():
    return render_template('test/base.html')


@bp.route('/serverlist')
def serverlist():
    page = request.args.get('page', 1, type=int)
    request_per_page = request.args.get('length', None, type=int)
    query = Server.query.order_by(Server.envinfo_id)
    pagination = query.paginate(page, per_page=request_per_page or current_app.config['FLASKY_POSTS_PER_PAGE'],
                                error_out=False)
    servers = pagination.items
    number = query.count()
    return render_template('test/serverlist.html', active_page='index', servers=servers, pagination=pagination,
                           number=number)


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
