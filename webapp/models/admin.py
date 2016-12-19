#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask_admin.contrib import sqla

from .user import User
from .server import Server

class UserAdmin(sqla.ModelView):
    column_labels = {
        'id': u'序号',
        'title': u'新闻标题',
        'timestamp': u'发布时间',
        'count': u'浏览次数',
        'content': u'新闻内容'
    }
    column_list = ('id', 'title', 'timestamp', 'count', 'content')

    def __init__(self, session, **kwargs):
        super(UserAdmin, self).__init__(User, session, **kwargs)


class ServerAdmin(sqla.ModelView):
    column_labels = {
        'id': '序号',
        'ip': 'ip',
        'project': '项目',
        'type': '机器类型',
        'oslevel': '操作系统版本',
        'use': '用途',
        'status': '状态',
        'contract_person': '联系人'
    }
    column_list = ('ip', 'project', 'type', 'oslevel', 'use', 'status', 'contract_person')

    def __init__(self, session, **kwargs):
        super(ServerAdmin, self).__init__(Server, session, **kwargs)
