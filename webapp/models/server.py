#!/usr/bin/env python
# coding: utf-8

__author__ = 'yueyt'

from webapp import db
from .user import Subproject


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15), unique=True, nullable=False)
    type = db.Column(db.String(128))
    oslevel = db.Column(db.String(32))
    use = db.Column(db.String(128))
    status = db.Column(db.String(5))
    owner = db.Column(db.String(32))

    # 关联表
    envinfo_id = db.Column(db.Integer, db.ForeignKey('envinfo.id'))
    serverusers = db.relationship('ServerUser', backref='server', lazy='dynamic')

    def __repr__(self):
        return '<Server: ip:{} use:{}>'.format(self.ip, self.use)

    @staticmethod
    def generate_fake(count=1000):
        print('insert Server records:{}'.format(count))
        from random import choice

        envinfos = Envinfo.query.all()
        subprojects_list = Subproject.query.all()
        ip_sublist = [str(i) for i in range(1, 254)]
        for i in range(count):
            s = '.'.join([choice(ip_sublist), choice(ip_sublist), choice(ip_sublist), choice(ip_sublist)])
            s = Server(ip=s, type='PC', oslevel='AIX 7100')
            s.envinfo_id = choice(envinfos).id
            sb = choice(subprojects_list)
            s.subprojects.append(sb)

            try:
                db.session.add(s)
            except:
                db.session.rollback()
            else:
                db.session.commit()

    @property
    def get_subproject(self):
        return [self.subprojects]

    @property
    def get_subproject_id(self):
        return [sb.id for sb in self.subprojects]

    @property
    def get_subproject_name(self):
        return ''.join([sb.name for sb in self.subprojects])

    def to_json(self):
        json_server = {
            'subprojects': self.get_subproject_name,
            'envinfo': ' '.join([self.envinfo.location, self.envinfo.envname]),
            'ip': self.ip,
            'oslevel': self.oslevel,
            'owner': self.owner,
            'id':self.id
        }
        return json_server


class Envinfo(db.Model):
    '''环境信息'''
    id = db.Column(db.Integer, primary_key=True)
    envname = db.Column(db.String(64), nullable=False)
    location = db.Column(db.String(32))
    color = db.Column(db.String(10))
    describe = db.Column(db.String(64))
    servers = db.relationship('Server', backref='envinfo', lazy='dynamic')

    def __repr__(self):
        return '<Env: {} {} {}>'.format(self.id, self.location, self.envname)

    @staticmethod
    def insert_envinfo():
        from sqlalchemy import and_
        envnames = ['DEV', 'SIT', 'UAT', 'TRL', 'QUS']
        locations = ['境内', '海外', '离岸', '港行']
        for l in locations:
            for e in envnames:
                res = Envinfo.query.filter(and_(Envinfo.envname == e, Envinfo.location == l)).all()
                if res:
                    continue
                ev = Envinfo(envname=e, location=l, describe=' '.join([l, e]))
                print(ev)
                db.session.add(ev)
                db.session.commit()

    __table_args__ = (db.UniqueConstraint('envname', 'location', name='ix_envname_location'),)


class Appinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appname = db.Column(db.String(32), nullable=False)
    describe = db.Column(db.String(128))


class Software(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    softname = db.Column(db.String(32), nullable=False)
    version = db.Column(db.String(32), nullable=False)


class ServerUser(db.Model):
    '''服务器登录用户信息'''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    desc = db.Column(db.String(64))
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'))

    @staticmethod
    def generate_fake():
        servers = Server.query.all()
        for s in servers:
            su1 = ServerUser(server_id=s.id, username='root', password='123456')
            su2 = ServerUser(server_id=s.id, username='mqm', password='mqm')
            su3 = ServerUser(server_id=s.id, username='egspadm', password='egspadm')
            db.session.add(su1)
            db.session.add(su2)
            db.session.add(su3)
        db.session.commit()
