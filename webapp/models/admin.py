#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask_admin.contrib.sqla import ModelView

from webapp import admin
from webapp import db
from webapp.models.user import User

admin.add_view(ModelView(User), db.session())
