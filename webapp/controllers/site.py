#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import Blueprint, redirect, url_for, request, current_app, flash
from flask import render_template

from webapp.forms.user import LoginForm
from webapp.models.server import Server

bp = Blueprint('site', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    query = Server.query
    pagination = query.paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                error_out=False)

    servers = pagination.items
    number = query.count()
    return render_template('index.html', active_page='index', servers=servers, pagination=pagination,
                           number=number)


@bp.route('/search', methods=['GET', 'POST'])
def search():
    q = request.args.get('q').strip()
    page = request.args.get('page', 1, type=int)
    query = Server.query.filter(Server.ip.like(q))
    pagination = query.paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                error_out=False)
    servers = pagination.items
    flash('有{}条符合条件的记录'.format(query.count()))
    return render_template('index.html', active_page='index', servers=servers, pagination=pagination)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return redirect(url_for('.index'))
