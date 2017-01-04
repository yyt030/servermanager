#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from webapp import db
from webapp import login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(32))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

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


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(32), nullable=False)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.LOGIN, True),
            'Moderator': (Permission.LOGIN | Permission.ADD | Permission.EDITOR, False),
            'PM': (Permission.LOGIN | Permission.ADD | Permission.EDITOR | Permission.LOGIN | Permission.DELETE, False),
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
    ADD = 0b00000001  # 添加
    DELETE = 0b00000010  # 删除
    EDITOR = 0b00000100  # 编辑
    LOGIN = 0b00001000  # 远程登录
    ADMINISTER = 0b10000000  # 管理


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
    id = db.Column(db.Integer, primary_key=True)
    opertype = db.Column(db.Integer, primary_key=False)
    operlog = db.Column(db.String)
