# coding: utf8
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASKY_POSTS_PER_PAGE = 15
    FLASKY_SLOW_DB_QUERY_TIME = 0.5

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    BOOTSTRAP_SERVE_LOCAL = True

    CACHE_DEFAULT_TIMEOUT = 60
    DOWNLOAD_DEFAULT_DEST = os.path.join(basedir, 'download')

    SAVE_IMAGE_DEST = os.path.join(basedir, 'webapp/static/images/qa_images')

    WHOOSH_BASE = os.path.join(basedir, 'search.db')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'servermanager.sqlite')

    # for redis cache
    CACHE_TYPE = 'simple'


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
