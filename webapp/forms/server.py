#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, TextAreaField,PasswordField
from wtforms import ValidationError
from wtforms.validators import ip_address

from webapp.models.server import Envinfo, Server


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
        super(ServerForm, self).__init__(*args, **kwargs)

        _machine_type_list = [
            ('SUSE SLES11 SP2', 'SUSE SLES11 SP2'),
            ('SUSE SLES11 SP3', 'SUSE SLES11 SP3'),
            ('SUSE SLES11 SP4', 'SUSE SLES11 SP4'),
            ('AIX 7100', 'AIX 7100'),
            ('AIX 5100', 'AIX 5100'),
            ('AIX 6100', 'AIX 6100')
        ]
        _project_list = [
            ('BGSP', 'BGSP'), ('EGSP', 'EGSP')
        ]
        self.project.choices = _project_list
        self.project.coerce = str
        self.oslevel.choices = _machine_type_list
        self.oslevel.coerce = str
        self.envinfo_id.choices = [(a.id, ' '.join([a.location, a.envname])) for a in Envinfo.query.order_by('id')]

    def validate_ip(self, field):
        if Server.query.filter_by(ip=field.data).first():
            raise ValidationError('该ip已经登记过！')


class ServerUserForm(FlaskForm):
    username = StringField('用户名')
    password = PasswordField('密码')
    submit_add = SubmitField('保存密码')
    submit_delete = SubmitField('删除密码')