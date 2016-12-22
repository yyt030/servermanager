#!/usr/bin/env python
# coding: utf8

import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from webapp import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def init_test_data():
    """初始化相关测试数据"""
    from webapp.models.server import Server, Envinfo
    Server.generate_fake(10)


@manager.command
def init_static_data():
    """初始化相关静态数据"""
    from webapp.models.server import Envinfo
    Envinfo.generate_fake()


if __name__ == '__main__':
    manager.run()
