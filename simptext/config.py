# -*- coding: utf-8 -*-
"""
 CONFIGLE

 @author wenlong
"""
import os
_basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'development version'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir,'simptext.db')
    USERNAME = 'admin'
    PASSWORD = 'admin'


class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True

class TestingConfig(Config):
    Testing = True
