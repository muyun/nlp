# -*- coding: utf-8 -*-
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort,\
    render_template, flash

# the application
app = Flask(__name__)
app.config.from_object(__name)

# load default config
app.config.update(dict(
    # the Database Path
    DATABASE=os.path.join(app.root_path,'simptext.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


# database
def connect_db():
    """ database connection"""
    rv = sqlite3.connect(app.config['DATABASE'])
    # row
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """ opens a new database connection
