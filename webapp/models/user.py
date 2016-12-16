#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from webapp import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    hash_password = db.Column(db.String(128))
    email = db.Column(db.String(32))


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(32), nullable=False)


class Operation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opertype = db.Column(db.Integer, primary_key=False)
    operlog = db.Column(db.String)

