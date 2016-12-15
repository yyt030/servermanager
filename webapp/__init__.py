# coding: utf8

from flask import Flask, render_template, g
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

moment = Moment()
db = SQLAlchemy()
bootstrap = Bootstrap()

from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    # from .controllers import question, site, user, tag
    # from .api import user as user_api

    # app.register_blueprint(question.bp, url_prefix='/q')
    # app.register_blueprint(tag.bp, url_prefix='/t')
    # app.register_blueprint(user_api.bp, url_prefix='/api')
    # app.register_blueprint(user.bp, url_prefix='/u')
    # app.register_blueprint(site.bp, url_prefix='')

    # 注册错误展示页面
    register_error_handle(app)

    # 注册搜索引擎
    # from .models.question import Question, Answer, Tag


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
