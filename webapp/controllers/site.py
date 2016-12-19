#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import Blueprint, redirect, url_for, request, current_app
from flask import render_template
from flask_login import current_user

from webapp import db
from webapp.forms.server import ServerForm
from webapp.forms.user import LoginForm
from webapp.models.server import Server
from webapp.models.user import Permission

bp = Blueprint('site', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = ServerForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        server = Server(ip=form.ip.data,
                        author=current_user._get_current_object())
        db.session.add(server)
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)

    query = Server.query
    pagination = query.paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    servers = pagination.items
    return render_template('index.html', form=form, servers=servers, pagination=pagination)


@bp.route('/search', methods=['GET', 'POST'])
def search():
    return redirect(url_for('.index'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return redirect(url_for('.index'))
