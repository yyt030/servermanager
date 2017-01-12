#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, InputRequired, Length, Email

from webapp.models.user import Role, Subproject


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64)], render_kw={'placeholder': '邮箱的用户名'})
    password = PasswordField('密码', validators=[DataRequired()],
                             render_kw={'placeholder': 'XXXXXX。。。'})
    remember_me = BooleanField('记住我', default=True)
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[InputRequired(), Length(1, 64)], description='字母、数字等，用户名唯一')
    email = StringField('邮箱', validators=[InputRequired(), Length(1, 64),
                                          Email()], description='hello@xxx.com')
    password = PasswordField('密码', validators=[InputRequired(), Length(1, 64)], description='不少于 6 位')
    submit = SubmitField('注册')


class EditProfileForm(FlaskForm):
    username = StringField('用户名', validators=[InputRequired(), Length(1, 64)])
    email = StringField('邮箱', validators=[InputRequired(), Length(1, 64),
                                          Email()], render_kw={'placeholder': 'hello@xxx.com'})
    role_id = SelectField('权限', validators=[InputRequired()], coerce=int)
    subproject_id = SelectMultipleField('所属项目:', coerce=int)

    sumit = SubmitField('修改')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role_id.choices = [(r.id, ' '.join([r.rolename, str(r.permissions)])) for r in
                                Role.query.order_by('id').all()]
        self.subproject_id.choices = [(a.id, ' '.join([a.name, a.name_en])) for a in Subproject.query.order_by('id')]
