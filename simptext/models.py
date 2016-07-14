# -*- coding: utf-8 -*-
"""
  Data Model -
"""

from app import db

class Entry(db.Model):
        __tablename = 'entries'
        
        id = db.Column(db.Integer, primary_key=True)
        text = db.Column(db.String(480))

        def __init__(self, text):
            self.text = text

        # a __repr__() method to represent the object when we query for it.
        def __repr__(self):
            return '<Text %r>' % self.text

