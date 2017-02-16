#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from marshmallow import fields, Schema


class ProjectServerDashboardSchema(Schema):
    # res = {
    #     'categories': ['P1', 'P2', 'P3'],
    #     'series': [{
    #         'type': 'column',
    #         'name': 'P1',
    #         'data': [
    #             {'name': 'P1', 'y': 20, 'drilldown': 'P1'}
    #         ]
    #     }, {
    #         'type': 'column',
    #         'name': 'P2',
    #         'data': [
    #             {'name': 'P2', 'y': 30, 'drilldown': 'P2'}
    #         ]
    #     },
    #         {
    #             'type': 'column',
    #             'name': 'P3',
    #             'data': [
    #                 {'name': 'P3', 'y': 40, 'drilldown': 'P2'}
    #             ]
    #         }
    #     ]
    # }
    categories = fields.List
    series = fields.List


class SeriesBase(Schema):
    type = fields.Str
    name = fields.Str
    data = fields.List


class SeriesDataBase(Schema):
    name = fields.Str
    y = fields.Int
    drilldown = fields.Str
