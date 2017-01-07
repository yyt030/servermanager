#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import Blueprint, render_template
from flask_login import current_user

from webapp import db
from webapp.forms.user import ProfileForm

bp = Blueprint('u', __name__)


@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    profileform = ProfileForm()
    if profileform.validate_on_submit():
        current_user.email = profileform.email.data
        current_user.role_id = profileform.role_id.data

        db.session.add(current_user)
        db.session.commit()
    profileform.email.data = current_user.email
    profileform.username.data = current_user.username
    profileform.role_id.data = current_user.role_id

    return render_template('profile.html', profileform=profileform)


@bp.route('/edit')
def edit_profile():
    pass
