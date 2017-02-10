#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import redirect, url_for, request
from flask_admin.contrib import sqla
from flask_login import current_user

from .server import Server, ServerUser
from .user import User


class UserAdmin(sqla.ModelView):
    column_labels = {
        'id': u'序号',
        'username': u'用户名',
        'password_hash': u'密码',
        'email': u'邮箱',
        'rolename': u'权限id',
    }
    column_list = ('id', 'username', 'password_hash', 'email', 'role.rolename')

    def __init__(self, session, *args, **kwargs):
        super().__init__(User, session, *args, **kwargs)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_administrator()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('site.login', next=request.url))


class ServerAdmin(sqla.ModelView):
    column_labels = {
        'id': '序号',
        'ip': 'ip',
        'project': '项目',
        'type': '机器类型',
        'oslevel': '操作系统版本',
        'use': '用途',
        'status': '状态',
        'owner': '联系人'
    }
    column_list = ('ip', 'project', 'type', 'oslevel', 'use', 'status', 'owner')

    def __init__(self, session, **kwargs):
        super(ServerAdmin, self).__init__(Server, session, **kwargs)


class ServerUserAdmin(sqla.ModelView):
    column_labels = {
        'id': '序号',
        'username': '用户名',
        'password': '密码',
        'role_id': '权限'
    }
    column_list = ('ip', 'username', 'password', 'role_id')

    def __init__(self, session, **kwargs):
        super(ServerUserAdmin, self).__init__(ServerUser, session, **kwargs)
