#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import Blueprint
from flask_restful import Resource

api_bp = Blueprint('api', __name__)


class FooApi(Resource):
    def get(self):
        return 'get ok'

    def post(self):
        return 'post ok'
