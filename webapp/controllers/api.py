#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'
from flask import Blueprint
from flask_restful import Resource, fields, marshal_with

bp = Blueprint('api', __name__)

resource_fields = {
    'task': fields.String,
    'uri': fields.Url('api.foo')
}


class TodoDao(object):
    def __init__(self, todo_id, task):
        self.todo_id = todo_id
        self.task = task

        # This field will not be sent in the response
        self.status = 'active'


class FooApi(Resource):
    @marshal_with(resource_fields)
    def get(self, **kwargs):
        return TodoDao(todo_id='my_todo', task='Remember the milk')

    def post(self):
        return 'post ok'
