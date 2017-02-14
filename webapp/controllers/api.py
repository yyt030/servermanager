#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'
from flask import Blueprint, request, current_app, jsonify
from flask_restful import Resource

bp = Blueprint('api', __name__)

from webapp.models.server import Server
from webapp import db


class ServerListApi(Resource):
    def get(self):
        start = request.args.get('start', 0, type=int)
        page_size = request.args.get('length', current_app.config['FLASKY_POSTS_PER_PAGE'], type=int)

        search_value = request.args.get('search[value]')
        if search_value:
            query = Server.query.filter(
                Server.ip.like('%{}%'.format(search_value))).order_by(Server.envinfo_id)
        else:
            query = Server.query.order_by(Server.envinfo_id)

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
    def get(self, id):
        id = request.args.get('id')
        pass

    def delete(self, ip):
        # /api/servers/96.141.235.232
        server = Server.query.filter(Server.ip == ip).first()
        if server:
            db.session.delete(server)
            db.session.commit()
