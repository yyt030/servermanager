#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'
from flask import request, session


def make_cache_key():
    path = request.path
    args = str(hash('{}{}'.format(frozenset(request.args.items()), session.get('_flashes'))))
    return (path + args).encode('utf-8')
