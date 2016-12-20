#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import ip_address


class ServerForm(FlaskForm):
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
    ip = StringField('ip:', validators=[ip_address()])
    project = SelectField('所属项目:', choices=_project_list, coerce=str)
    oslevel = SelectField('操作系统版本:', choices=_machine_type_list, coerce=str, default='SUSE SLES11 SP3')
    use = TextAreaField('用途:')
    contract_person = StringField('联系人:')
    status = BooleanField('使用中', default=True)

    submit = SubmitField('保存')
