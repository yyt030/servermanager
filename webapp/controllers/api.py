#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'
from flask import Blueprint, request, current_app, jsonify
from flask_restful import Resource
from sqlalchemy import desc, asc

bp = Blueprint('api', __name__)

from webapp.models.server import Server
from webapp import db


class ServerListApi(Resource):
    def get(self):
        start = request.args.get('start', 0, type=int)
        page_size = request.args.get('length', current_app.config['FLASKY_POSTS_PER_PAGE'], type=int)

        # search
        search_value = request.args.get('search[value]')
        if search_value:
            query = Server.query.filter(
                Server.ip.like('%{}%'.format(search_value)))
        else:
            query = Server.query.order_by(Server.envinfo_id)

        # order by
        order_col_num = request.args.get('order[0][column]', type=int)
        if order_col_num:
            order_dir = request.args.get('order[0][dir]', type=str, default='asc')
            order_col = request.args.get('columns[{}][data]'.format(order_col_num))
            if order_dir == 'desc':
                query = query.order_by(desc('{}'.format(order_col)))
            else:
                query = query.order_by(asc('{}'.format(order_col)))

        pagination = query.paginate((start + 1) / page_size, per_page=page_size, error_out=False)
        servers = pagination.items
        record_total = query.count()

        result = {
            "draw": request.args.get('draw', 1, type=int),
            "recordsTotal": record_total,
            "recordsFiltered": record_total,
            "data": [server.to_json() for server in servers]
        }
        return jsonify(result)

    def delete(self):
        serverlist = request.form.get('ips')
        servers = Server.query.filter(Server.ip.in_(serverlist.split(',')))
        for s in servers:
            db.session.delete(s)
        db.session.commit()


class ServerApi(Resource):
    def get(self, ip):
        server = Server.query.filter(Server.ip == ip).first()
        return server.to_json()

    def delete(self, ip):
        # /api/servers/96.141.235.232
        server = Server.query.filter(Server.ip == ip).first()
        if server:
            db.session.delete(server)
            db.session.commit()


class ProjectServerDashboard(Resource):
    def get(self):
        res = {
            'categories': ['P1', 'P2', 'P3'],
            'series': [{
                'type': 'column',
                'name': 'P1',
                'data': [
                    {'name': 'P1', 'y': 20, 'drilldown': 'P1'}
                ]
            }, {
                'type': 'column',
                'name': 'P2',
                'data': [
                    {'name': 'P2', 'y': 30, 'drilldown': 'P2'}
                ]
            },
                {
                    'type': 'column',
                    'name': 'P3',
                    'data': [
                        {'name': 'P3', 'y': 40, 'drilldown': 'P2'}
                    ]
                }
            ]
        }
        print('>>>', res)
        return jsonify(res)
