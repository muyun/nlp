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
        wordlevel = db.Column(db.String(2), index=True)
        algs = db.Column(db.String(16), index=True)
        
        def __init__(self, text, words, wordlevel, algs):
            self.text = text
            self.words = words
            self.wordlevel = wordlevel
            self.algs = algs
            
        # a __repr__() method to represent the object when we query for it.
        def __repr__(self):
            return '%s' % (self.text + "@" + self.words + "@" + self.wordlevel + "@" + self.algs)

class Setting(db.Model):
        __tablename = 'setting'
        
        id = db.Column(db.Integer, primary_key=True)
        words = db.Column(db.String(960), index=True)
        wordlevel = db.Column(db.String(2), index=True)
        algs = db.Column(db.String(16), index=True)

        def __init__(self, words, wordlevel, algs):
            self.words = words
            self.wordlevel = wordlevel
            self.algs = algs

        # a __repr__() method to represent the object when we query for it.
        def __repr__(self):
            return '%s' % (self.words + "@" + self.wordlevel + "@" + self.algs)          

