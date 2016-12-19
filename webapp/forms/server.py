#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ip_address


class ServerForm(FlaskForm):
    ip = StringField('ip', validators=[ip_address()])
    submit = SubmitField('保存')
