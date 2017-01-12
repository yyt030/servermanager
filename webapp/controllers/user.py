#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import Blueprint, render_template, flash, abort, request, current_app
from flask_login import current_user

from webapp import db, cache, webssh_addr
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
    return render_template('user_edit.html', form=form)


@bp.route('/project')
def project():
    user = current_user
    page = request.args.get('page', 1, type=int)
    query = Subproject.query.join(Project).filter(Project.pm_userid == user.id)
    pagination = query.paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                error_out=False)
    subprojects = pagination.items
    flash('有{}条符合条件的记录'.format(query.count()))
    return render_template('project_list.html', active_page='index',
                           subprojects=subprojects, pagination=pagination)


@bp.route('/project/users')
def project_users():
    subproject_id = request.args.get('id')
    sb = Subproject.query.get_or_404(subproject_id)
    users = sb.user_subproject.all()
    return render_template('user_list.html', users=users)
