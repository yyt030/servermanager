#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import Blueprint, render_template, flash, abort
from flask_login import current_user

from webapp import db, cache
from webapp.forms.user import EditProfileForm
from webapp.models.user import User, Project, Subproject

bp = Blueprint('u', __name__)


@bp.route('/<username>')
def user(username):
    user = User.query.filter(User.username == username).first()
    if user is None:
        abort(404)

    return render_template('user_info.html', user=user)


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def profile(id):
    user = User.query.get_or_404(id)
    form = EditProfileForm()
    if form.validate_on_submit():
        user.email = form.email.data
        user.role_id = form.role_id.data

        db.session.add(user)
        db.session.commit()
        cache.clear()

        flash('信息已经更新')
    form.email.data = user.email
    form.username.data = user.username
    form.role_id.data = user.role_id
    return render_template('edit_user.html', form=form)


@bp.route('/projects')
def project():
    user = current_user
    subp = Subproject.query.join(Project).filter(Project.pm_userid == user.id).all()
    users = []
    for sb in subp:
        users.append(*sb.users.all())
    return render_template('user_list.html', users=users)
