#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import Blueprint, redirect, url_for
from flask import render_template

from webapp.forms.user import LoginForm

bp = Blueprint('site', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('base.html')


@bp.route('/search', methods=['GET', 'POST'])
def search():
    return redirect(url_for('.index'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('base.html', form=form)
