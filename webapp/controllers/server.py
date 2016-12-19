#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'
from flask import Blueprint, render_template

from webapp.forms.server import ServerForm

bp = Blueprint('s', __name__)


@bp.route('/create')
def create():
    name = None
    form = ServerForm()
    if form.validate_on_submit():
        name = form.ip.data
        pass

    return render_template('create.html', active_page='add', form=form, name=name)
