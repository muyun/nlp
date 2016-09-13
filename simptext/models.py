# -*- coding: utf-8 -*-
"""
  Data Model - store data
"""

from app import db

class Entry(db.Model):
        __tablename = 'entries'
        
        id = db.Column(db.Integer, primary_key=True)
        text = db.Column(db.String(960), index=True)
        words = db.Column(db.String(960), index=True)

        def __init__(self, text, words):
            self.text = text
            self.words = words

        # a __repr__() method to represent the object when we query for it.
        def __repr__(self):
            return '<Text %r>' % (self.text + "@" + self.words)

class Setting(db.Model):
        __tablename = 'setting'
        
        id = db.Column(db.Integer, primary_key=True)
        text = db.Column(db.String(960), index=True)
        words = db.Column(db.String(960), index=True)

        def __init__(self, text, words):
            self.text = text
            self.words = words

        # a __repr__() method to represent the object when we query for it.
        def __repr__(self):
            return '<Text %r>' % (self.text + "@" + self.words)          

