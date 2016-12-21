#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import Blueprint, redirect, url_for, request, current_app
from flask import render_template

from webapp.forms.user import LoginForm
from webapp.models.server import Server

bp = Blueprint('site', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    query = Server.query
    pagination = query.paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    servers = pagination.items
    return render_template('index.html', active_page='index', servers=servers, pagination=pagination)


@bp.route('/search', methods=['GET', 'POST'])
def search():
    return redirect(url_for('.index'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return redirect(url_for('.index'))
