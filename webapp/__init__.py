# coding: utf8

import socket

from flask import Flask, render_template
from flask_admin import Admin
from flask_bootstrap import Bootstrap
from flask_cache import Cache
from flask_login import LoginManager
from flask_moment import Moment
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

try:
    ip = socket.gethostbyname(socket.gethostname())
except:
    ip = '127.0.0.1'

webssh_addr = '{}:{}'.format(ip, 9527)

moment = Moment()
db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
cache = Cache()
admin = Admin(template_mode='bootstrap3')
from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # init app
    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    admin.init_app(app)
    login_manager.init_app(app)
    cache.init_app(app)

    # 注册flask-admin视图
    register_admin_view()

    # blueprint
    from webapp.controllers import site, server
    app.register_blueprint(site.bp)
    app.register_blueprint(server.bp, url_prefix='/servers')

    # restful api
    from webapp.controllers import api
    restful_api = Api(api.bp)
    restful_api.add_resource(api.ServerListApi, '/servers', endpoint='servers')
    restful_api.add_resource(api.ServerApi, '/servers/<string:ip>', endpoint='server')
    restful_api.add_resource(api.DashBoardApi, '/dashboard', endpoint='dashboard')

    app.register_blueprint(api.bp, url_prefix='/api')

    # 注册错误展示页面
    register_error_handle(app)

    return app


def register_error_handle(app):
    """添加HTTP错误页面"""
    from flask import redirect, url_for
    @app.errorhandler(401)
    def page_401(error):
        # return render_template('site..html'), 401
        return redirect(url_for('site.login'))

    @app.errorhandler(403)
    def page_403(error):
        return render_template('403.html'), 403

    @app.errorhandler(404)
    def page_404(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def page_500(error):
        return render_template('500.html'), 500


# flask 添加admin视图
def register_admin_view():
    from webapp.models.admin import UserAdmin

    # admin.add_view(ServerUserAdmin(db.session))
    admin.add_view(UserAdmin(db.session))
