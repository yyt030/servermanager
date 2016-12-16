#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from webapp import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projname = db.Column(db.String(64), nullable=False)
    pm = db.Column(db.String(64))

