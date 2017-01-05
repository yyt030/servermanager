#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, TextAreaField, PasswordField
from wtforms import ValidationError
from wtforms.validators import ip_address

from webapp.models.server import Envinfo, Server

MACHINE_TYPE_LIST = [
    ('SUSE SLES11 SP2', 'SUSE SLES11 SP2'),
    ('SUSE SLES11 SP3', 'SUSE SLES11 SP3'),
    ('SUSE SLES11 SP4', 'SUSE SLES11 SP4'),
    ('AIX 7100', 'AIX 7100'),
    ('AIX 5100', 'AIX 5100'),
    ('AIX 6100', 'AIX 6100')
]
PROJECT_LIST = [
    ('BGSP', 'BGSP'), ('EGSP', 'EGSP')
]


class ServerForm(FlaskForm):
    ip = StringField('ip:', validators=[ip_address()], render_kw={'placeholder': 'ip: XXX.XXX.XXX.XXX'})
    project = SelectField('所属项目:')
    oslevel = SelectField('操作系统版本:')
    use = TextAreaField('用途:', render_kw={'placeholder': '填写该机器主要做什么用？MB应用/MQ网关。。。'})
    contract_person = StringField('联系人:', render_kw={'placeholder': '填写机器的申请人'})
    envinfo_id = SelectField('环境:', coerce=int)
    status = BooleanField('使用中', default=True)
    submit = SubmitField('保存')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.project.choices = PROJECT_LIST
        self.project.coerce = str
        self.oslevel.choices = MACHINE_TYPE_LIST
        self.oslevel.coerce = str
        self.envinfo_id.choices = [(a.id, ' '.join([a.location, a.envname])) for a in Envinfo.query.order_by('id')]

    def validate_ip(self, field):
        if Server.query.filter_by(ip=field.data).first():
            raise ValidationError('该ip已经登记过！')


class EditServerForm(FlaskForm):
    ip = StringField('ip:', render_kw={'readonly': 'readonly'})
    project = SelectField('所属项目:')
    oslevel = SelectField('操作系统版本:')
    use = TextAreaField('用途:', render_kw={'placeholder': '填写该机器主要做什么用？MB应用/MQ网关。。。'})
    contract_person = StringField('联系人:', render_kw={'placeholder': '填写机器的申请人'})
    envinfo_id = SelectField('环境:', coerce=int)
    status = BooleanField('使用中', default=True)
    submit = SubmitField('保存')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project.choices = PROJECT_LIST
        self.project.coerce = str
        self.oslevel.choices = MACHINE_TYPE_LIST
        self.oslevel.coerce = str
        self.envinfo_id.choices = [(a.id, ' '.join([a.location, a.envname])) for a in Envinfo.query.order_by('id')]


class ServerUserForm(FlaskForm):
    username = StringField('用户名')
    password = PasswordField('密码')
    submit_add = SubmitField('保存密码')
    submit_delete = SubmitField('删除密码')
