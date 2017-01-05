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
    from webapp.models.server import Server
    from webapp.models.user import Project, Subproject
    print('insert Project...')
    Project.generate_fake()
    print('insert Subproject...')
    Subproject.generate_fake()
    print('insert Server...')
    Server.generate_fake()


@manager.command
def init_static_data():
    """初始化相关静态数据
        1: 环境
        2：角色
        3: 用户
        4：项目
        5：子项目
        6：服务器
    """
    from webapp.models.server import Envinfo
    from webapp.models.user import Role, User
    print('insert Envinfo...')
    Envinfo.insert_envinfo()
    print('insert Role...')
    Role.insert_roles()
    print('insert admin...')
    User.insert_admin_user()
    print('insert User...')
    User.generate_fake(10)


if __name__ == '__main__':
    manager.run()
