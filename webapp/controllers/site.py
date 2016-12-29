#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import (Blueprint, redirect, url_for, request, current_app, flash, g, abort)
from flask import render_template

from webapp import db
from webapp.forms.user import LoginForm
from webapp.models.server import Server, Envinfo
import json

bp = Blueprint('site', __name__)


@bp.before_app_request
def before_request():
    locations = db.session.query(Envinfo.location.distinct()).order_by(Envinfo.id).all()
    envnames = db.session.query(Envinfo.envname.distinct()).order_by(Envinfo.id).all()
    g.locations = [l[0] for l in locations]
    g.envnames = [e[0] for e in envnames]


@bp.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', None)
    if sort:
        query = None
        v = request.args.get('v', '')
        if sort == 'envname':
            query = Server.query.join(Envinfo).filter(Envinfo.envname == v).order_by(Envinfo.location)
        elif sort == 'location':
            query = Server.query.join(Envinfo).filter(Envinfo.location == v).order_by(Envinfo.envname)
        else:
            abort(404)
    else:
        query = Server.query.order_by(Server.envinfo_id)

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
    query = Server.query.filter(Server.ip.like('%{}%'.format(q)))
    pagination = query.paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                error_out=False)
    servers = pagination.items
    flash('有{}条符合条件的记录'.format(query.count()))
    return render_template('search_list.html', active_page='index', servers=servers, pagination=pagination)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return redirect(url_for('.index'))

@bp.route('/Dysearch',methods=['GET','POST'])
def Dysearch():

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


    print(Jsonstr)
    return Jsonstr
