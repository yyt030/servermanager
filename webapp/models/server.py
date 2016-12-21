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
        return '<Server: ip:{} use:{}>'.format(self.ip, self.use)

    @staticmethod
    def generate_fake():
        for i in range(1, 185):
            for j in range(1, 5):
                for k in range(1, 5):
                    s = '.'.join([str(i), str(j), str(k), '1'])
                    s = Server(ip=s, project='bgsp', type='pc', oslevel='aix 7100')
                    try:
                        db.session.add(s)
                    except:
                        db.session.rollback()
                    finally:
                        db.session.commit()
                    print('*' * 10, s)


class Envinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    envname = db.Column(db.String(64), nullable=False)
    describe = db.Column(db.String(64))

    def __repr__(self):
        return '<Env: {} {}>'.format(self.id, self.envname)


class Appinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appname = db.Column(db.String(32), nullable=False)
    describe = db.Column(db.String(128))


class software(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    softname = db.Column(db.String(32), nullable=False)
    version = db.Column(db.String(32), nullable=False)
