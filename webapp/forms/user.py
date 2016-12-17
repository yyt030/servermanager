#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, Email


class LoginForm(Form):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64),
                                          Email()], description='hello@xxx.com')
    password = PasswordField('密码', validators=[DataRequired()], description='密码')
    remember_me = BooleanField('记住登录状态', default=True)
    submit = SubmitField('登录')


class RegisterForm(Form):
    username = StringField('用户名', validators=[InputRequired(), Length(1, 64)], description='字母、数字等，用户名唯一')
    email = StringField('邮箱', validators=[InputRequired(), Length(1, 64),
                                          Email()], description='hello@xxx.com')
    password = PasswordField('密码', validators=[InputRequired(), Length(1, 64)], description='不少于 6 位')
    submit = SubmitField('注册')
