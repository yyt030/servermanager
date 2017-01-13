#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField, \
    TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length, Email

from webapp.models.user import Role, Subproject, User


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


class EditSubjectForm(FlaskForm):
    name = StringField('项目名称', validators=[DataRequired()], render_kw={'placeholder': ' 输入项目的中文名称'})
    name_en = StringField('英文简称', validators=[DataRequired(), Length(min=4, max=4)],
                          render_kw={'placeholder': '4位英文简称'})
    desc = TextAreaField('项目描述', render_kw={'placeholder': '一句话描述项目简介'})
    user_id = SelectMultipleField('项目组成员', coerce=int)
    submit = SubmitField('修改', render_kw={'placeholder': '一句话描述项目简介'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id.choices = [(a.id, a.username) for a in User.query.order_by('id')]
