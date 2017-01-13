#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import Blueprint, render_template, flash, abort, request, current_app, redirect, url_for
from flask_login import current_user
from flask_login import login_required

from webapp import db, cache, webssh_addr
from webapp.forms.user import EditProfileForm, EditSubjectForm
from webapp.models.user import User, Project, Subproject

bp = Blueprint('u', __name__)


@bp.route('/<username>')
@login_required
def user(username):
    user = User.query.filter(User.username == username).first()
    if user is None:
        abort(404)

    return render_template('user_info.html', user=user)


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def profile(id):
    user = User.query.get_or_404(id)
    form = EditProfileForm()
    if form.validate_on_submit():
        user.email = form.email.data
        user.role_id = form.role_id.data

        sbs = Subproject.query.filter(Subproject.id.in_(form.subproject_id.data)).all()
        user.user_subproject = []
        for sb in sbs:
            user.user_subproject.append(sb)

        db.session.add(user)
        db.session.commit()
        cache.clear()

        flash('信息已经更新')
        return redirect(url_for('.project_users', id=current_user.id))
    form.email.data = user.email
    form.username.data = user.username
    form.role_id.data = user.role_id
    form.subproject_id.data = user.get_subproject_id
    return render_template('user_edit.html', form=form)


@bp.route('/project')
@login_required
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


@bp.route('/sb/<int:id>', methods=['GET', 'POST'])
@login_required
def subproject(id):
    subproject = Subproject.query.get_or_404(id)
    form = EditSubjectForm()
    if form.validate_on_submit():
        subproject.name = form.name.data
        subproject.name_en = form.name_en.data
        subproject.desc = form.desc.data

        users = User.query.filter(User.id.in_(form.user_id.data)).all()
        subproject.user_subproject = []
        for u in users:
            subproject.user_subproject.append(u)
        db.session.add(subproject)
        db.session.commit()
        flash('项目组信息已更新')

    form.name_en.data = subproject.name_en
    form.name.data = subproject.name
    form.desc.data = subproject.desc
    form.user_id.data = subproject.get_user_id

    return render_template('subproject_edit.html', form=form)


@bp.route('/project/users')
@login_required
def project_users():
    subproject_id = request.args.get('id')
    sb = Subproject.query.get_or_404(subproject_id)
    users = sb.user_subproject.all()
    return render_template('user_list.html', users=users)


@bp.route('/project/servers')
@login_required
def project_servers():
    subproject_id = request.args.get('id')
    sb = Subproject.query.get_or_404(subproject_id)

    page = request.args.get('page', 1, type=int)
    query = sb.servers
    pagination = query.paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                error_out=False)
    servers = pagination.items
    number = query.count()
    return render_template('project_servers.html', servers=servers, pagination=pagination,
                           number=number, webssh_addr=webssh_addr)
