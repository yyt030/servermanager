#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from webapp import db


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15), unique=True, nullable=False)
    project = db.Column(db.String(128))
    type = db.Column(db.String(128))
    oslevel = db.Column(db.String(32))
    use = db.Column(db.String(128))
    status = db.Column(db.String(5))
    contract_person = db.Column(db.String(32))

    def __repr__(self):
        return '<Server: %s [%s]>'.format(self.ip, self.use)


class Envinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    envname = db.Column(db.String(64), nullable=False)
    describe = db.Column(db.String(64))

    def __repr__(self):
        return '<Env: %s %s>'.format(self.id, self.envname)


class Appinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appname = db.Column(db.String(32), nullable=False)
    describe = db.Column(db.String(128))


class software(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    softname = db.Column(db.String(32), nullable=False)
    version = db.Column(db.String(32), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    hash_password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(32), nullable=False)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(32), nullable=False)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projname = db.Column(db.String(64), nullable=False)
    pm = db.Column(db.String(64))


class Operation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opertype = db.Column(db.Integer, primary_key=False)
    operlog = db.Column(db.String)
