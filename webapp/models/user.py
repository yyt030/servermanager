#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from webapp import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    hashpasswd = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(32))
