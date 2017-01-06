#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from webapp import db
from webapp import login_manager


class User(UserMixin, db.Model):
    '''用户信息'''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(32))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    projects = db.relationship('Project', backref='user', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    @property
    def password(self):
        raise AttributeError('密码只读, 不能直接修改')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def insert_admin_user():
        admin = User.query.filter(User.username == 'admin').first()
        if not admin:
            admin = User(username='admin', email='test@test.com')
            admin.password = 'admin'
            role = Role.query.filter(Role.rolename == 'Adminstrator').first()
            admin.role_id = role.id
            db.session.add(admin)
            db.session.commit()

            u = User(username='test', email='test@test.com')
            u.password = 'admin'
            admin.role_id = role.id
            db.session.add(u)
            db.session.commit()

    @staticmethod
    def generate_fake(count=300):
        from random import choice

        for i in range(count):
            u = User(username='user{}'.format(i), email='test{}@test.com'.format(i))
            u.password = 'test'
            role = choice(Role.query.all())
            u.role_id = role.id
            db.session.add(u)
            db.session.commit()


class Role(db.Model):
    '''角色信息'''
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(32), nullable=False)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.SERVER_LOGIN, True),
            'Moderator': (Permission.SERVER_LOGIN
                          | Permission.SERVER_ADD
                          | Permission.SERVER_EDIT,
                          False),
            'PM': (
                Permission.SERVER_LOGIN |
                Permission.SERVER_ADD |
                Permission.SERVER_EDIT |
                Permission.SERVER_LOGIN |
                Permission.SERVER_DELETE,
                False),
            'Adminstrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(rolename=r).first()
            if role is None:
                role = Role(rolename=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
            print('insert data {}'.format(role))
        db.session.commit()

    def __repr__(self):
        return '<Role {}: {}>'.format(self.id, self.rolename)


class Permission(object):
    '''权限信息'''
    # Server
    SERVER_ADD = 0b00000001  # 添加server与server_user
    SERVER_DELETE = 0b00000010  # 删除server
    SERVER_EDIT = 0b00000100  # 编辑server与server_user
    SERVER_LOGIN = 0b00001000  # 远程登录server

    # User
    USER_GROUP_MANAGER = 0b00010000  # 管理本组的成员以及付权限
    USER_EDIT = 0b00100000  # 编辑用户信息

    ADMINISTER = 0b10000000  # 管理员


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Operation(db.Model):
    '''操作信息'''
    id = db.Column(db.Integer, primary_key=True)
    opertype = db.Column(db.Integer, primary_key=False)
    operlog = db.Column(db.String)


class Project(db.Model):
    '''项目组信息'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    name_en = db.Column(db.String(4), nullable=False)
    pm_userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    desc = db.Column(db.Text)
    subprojects = db.relationship('Subproject', backref='project', lazy='dynamic')

    @staticmethod
    def generate_fake(count=100):
        from random import choice
        print('insert project record:{}'.format(count))
        for i in range(count):
            proj = Project(name='项目组{}'.format(i), name_en='p{}'.format(i), desc='项目组')
            u = choice(User.query.all())
            proj.pm_userid = u.id
            db.session.add(proj)
            db.session.commit()


class Subproject(db.Model):
    '''子项目信息'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    name_en = db.Column(db.String(4), nullable=False)
    desc = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    servers = db.relationship('Server', backref='subproject', lazy='dynamic')

    @staticmethod
    def generate_fake(count=200):
        from random import choice
        print('insert subproject record:{}'.format(count))
        for i in range(count):
            subproj = Subproject(name='子项目组{}'.format(i), name_en='s{}'.format(i), desc='子项目组')
            p = choice(Project.query.all())
            subproj.project_id = p.id
            db.session.add(subproj)
            db.session.commit()
