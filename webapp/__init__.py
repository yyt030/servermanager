# coding: utf8

from flask import Flask, render_template
from flask_admin import Admin

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# from flask_login import LoginManager


moment = Moment()
db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
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

    # admin
    register_admin_view()

    # blueprint
    from webapp.controllers import site, server
    app.register_blueprint(site.bp, url_prefix='/')
    app.register_blueprint(server.bp, url_prefix='/s')

    # 注册错误展示页面
    register_error_handle(app)

    return app


def register_error_handle(app):
    """添加HTTP错误页面"""

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
    from webapp.models.admin import ServerAdmin

    # admin.add_view(ModelView(User, db.session))
    admin.add_view(ServerAdmin(db.session))
