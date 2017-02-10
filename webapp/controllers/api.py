#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'
from flask import Blueprint, request, current_app, jsonify
from flask_restful import Resource

bp = Blueprint('api', __name__)

from webapp.models.server import Server


class ServerListApi(Resource):
    def get(self):
        draw = request.args.get('draw', 1, type=int)
        start = request.args.get('start', 0, type=int)
        length = request.args.get('length', current_app.config['FLASKY_POSTS_PER_PAGE'], type=int)
        search_value = request.args.get('search[value]')

        query = Server.query.order_by(Server.envinfo_id)
        pagination = query.paginate((start / length), per_page=length, error_out=False)

        servers = pagination.items
        record_total = query.count()
        result = {
            "draw": request.args.get('draw', 1, type=int),
            "recordsTotal": record_total,
            "recordsFiltered": record_total,
            "data": [server.to_json() for server in servers]
        }
        return jsonify(result)


class ServerApi(Resource):
    def get(self, id):
        pass
