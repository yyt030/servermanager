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
    envinfo_id = db.Column(db.Integer, db.ForeignKey('envinfo.id'))

    def __repr__(self):
        return '<Server: ip:{} use:{}>'.format(self.ip, self.use)

    @staticmethod
    def generate_fake(count=100):
        import random
        n = 0
        for i in range(1, 185):
            for j in range(2, 3):
                for k in range(3, 4):
                    if n>=count:
                        break
                    s = '.'.join([str(i), str(j), str(k), '1'])
                    s = Server(ip=s, project='BGSP', type='PC', oslevel='AIX 7100')
                    e = random.choice(Envinfo.query.all())
                    s.envinfo_id = e.id
                    try:
                        db.session.add(s)
                    except:
                        db.session.rollback()
                    else:
                        db.session.commit()
                        print('*' * 10, s)
                        n += 1


class Envinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    envname = db.Column(db.String(64), nullable=False)
    location = db.Column(db.String(32))
    color = db.Column(db.String(10))
    describe = db.Column(db.String(64))
    servers = db.relationship('Server', backref='envinfo', lazy='dynamic')

    def __repr__(self):
        return '<Env: {} {} {}>'.format(self.id, self.location, self.envname)

    @staticmethod
    def generate_fake():
        envnames = ['DEV', 'SIT', 'UAT', 'TRL', 'QUS']
        locations = ['境内', '海外', '离岸', '港行']
        for l in locations:
            for e in envnames:
                ev = Envinfo(envname=e, location=l, describe=' '.join([l, e]))
                print(ev)
                try:
                    db.session.add(ev)
                except:
                    db.session.rollback()
                else:
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
