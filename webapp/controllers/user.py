#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import Blueprint, render_template
from webapp.forms.user import ProfileForm
from webapp.models.user import User
from flask_login import current_user

bp = Blueprint('u', __name__)


@bp.route('/profile')
def profile():
    profileform = ProfileForm()

    print(current_user.username, current_user.id)

    return render_template('profile.html', profileform=profileform)


@bp.route('/edit')
def edit_profile():
    pass
