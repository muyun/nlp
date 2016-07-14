# -*- coding: utf-8 -*-
"""
get a console and enter commands within your flask environment

"""

import os
import readline
from pprint import pprint

#from flask import *
from app import app, db
from models import Entry

app.config.from_object('config.DevelopmentConfig')

#create the tables and database
db.create_all()

