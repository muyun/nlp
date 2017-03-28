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
        algs = db.Column(db.String(64), index=True)
        cselect = db.Column(db.String(2), index=True)
        s1 = db.Column(db.String(960), index=True)
        s2 = db.Column(db.String(960), index=True)
        
        def __init__(self, text, words, wordlevel, algs, cselect, s1, s2):
            self.text = text
            self.words = words
            self.wordlevel = wordlevel
            self.algs = algs
            self.cselect = cselect
            self.s1 = s1
            self.s2 = s2
            
        # a __repr__() method to represent the object when we query for it.
        def __repr__(self):
            return '%s' % (self.text +  "@" + self.words + "@" + self.wordlevel + "@" + self.algs +  "@" + self.cselect + "@" + self.s1 + "@" + self.s2 )

class Param(db.Model):
        __tablename = 'params'
        
        id = db.Column(db.Integer, primary_key=True)
        words = db.Column(db.String, index=True)
        wordlevel = db.Column(db.String(2), index=True)
        algs = db.Column(db.String(16), index=True)
        cselect = db.Column(db.String(2), index=True)

        def __init__(self, words, wordlevel, algs, cselect):
            self.words = words
            self.wordlevel = wordlevel
            self.algs = algs
            self.cselect = cselect

        # a __repr__() method to represent the object when we query for it.
        def __repr__(self):
            return '%s' % (self.words + "@" + self.wordlevel + "@" + self.algs + "@" + self.cselect)          

