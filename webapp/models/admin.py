#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask_admin.contrib import sqla

from .user import User

class UserAdmin(sqla.ModelView):
    inline_models = (User,)
