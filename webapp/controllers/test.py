#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'
from flask import Blueprint, render_template, request, current_app

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
    query = Server.query.order_by(Server.envinfo_id)
    pagination = query.paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                error_out=False)
    servers = pagination.items
    number = query.count()
    return render_template('test/serverlist.html', active_page='index', servers=servers, pagination=pagination,
                           number=number)
