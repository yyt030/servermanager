#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import (Blueprint, redirect, url_for, request, current_app, flash, g, abort)
from flask import render_template

from webapp import db, webssh_addr, cache
from webapp.forms.user import LoginForm
from webapp.models.server import Server, Envinfo
from webapp.models.user import User

bp = Blueprint('site', __name__)


def make_cache_key():
    path = request.path
    args = str(hash(frozenset(request.args.items())))
    return (path + args).encode('utf-8')


@bp.before_app_request
@cache.cached()
def before_request():
    locations = db.session.query(Envinfo.location.distinct()).order_by(Envinfo.id).all()
    envnames = db.session.query(Envinfo.envname.distinct()).order_by(Envinfo.id).all()
    g.locations = [l[0] for l in locations]
    g.envnames = [e[0] for e in envnames]


@bp.route('/', methods=['GET', 'POST'])
@cache.cached(key_prefix=make_cache_key)
def index():
    page = request.args.get('page', 1, type=int)
    query = Server.query.order_by(Server.envinfo_id)
    pagination = query.paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                error_out=False)
    servers = pagination.items
    number = query.count()
    return render_template('index.html', active_page='index', servers=servers, pagination=pagination,
                           number=number, webssh_addr=webssh_addr)


@bp.route('/search', methods=['GET', 'POST'])
@cache.cached(key_prefix=make_cache_key)
def search():
    q = request.args.get('q')
    filter = request.args.get('filter')
    page = request.args.get('page', 1, type=int)
    # 搜索框查询
    query = None
    if q:
        query = Server.query.filter(Server.ip.like('%{}%'.format(q.strip())))
    # 首页左侧菜单查询和列表链接查询
    if filter:
        v = request.args.get('v')
        if filter == 'envname':
            query = Server.query.join(Envinfo).filter(Envinfo.envname == v).order_by(Envinfo.location)
        elif filter == 'location':
            query = Server.query.join(Envinfo).filter(Envinfo.location == v).order_by(Envinfo.envname)
        elif filter == 'project':
            query = Server.query.filter(Server.project == v).order_by(Server.id)
        elif filter == 'contract':
            query = Server.query.filter(Server.contract_person == v).order_by(Server.id)
        else:
            abort(404)

    if not q and not filter:
        return redirect(url_for('.index'))

    pagination = query.paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                error_out=False)
    servers = pagination.items
    flash('有{}条符合条件的记录'.format(query.count()))
    return render_template('search_list.html', active_page='index', servers=servers, pagination=pagination,
                           webssh_addr=webssh_addr)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user = User.query.all()
    return redirect(url_for('.index'))


@bp.route('/dysearch', methods=['GET', 'POST'])
@cache.cached(key_prefix=make_cache_key)
def dysearch():
    q = request.args.get('ip')
    servers = []
    Jsonstr = ""
    query = Server.query.filter(Server.ip.like('%{}%'.format(q))).all()
    for sv in query:
        servers.append(sv)

    for svr in servers:
        Jsonstr += svr.ip
        Jsonstr += ","
    Jsonstr += "1"
    return Jsonstr
