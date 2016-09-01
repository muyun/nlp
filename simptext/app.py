# -*- coding: utf-8 -*-
"""
 Logical Model

 @author wenlong
"""
import os

from flask import Flask, request, render_template, session, g, redirect, url_for, abort, \
    render_template, flash, jsonify

from flask_sqlalchemy import SQLAlchemy

import json

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# this model is the db model
import models

#from algs import simp
from simptext import dt_sent, wordcal
#import simptext

#words = dt_sent.read_xlsx_file('./dataset/wordlist.xlsx', 1)
words = dt_sent.get_edblist('simptext/dataset/EDB_List.txt')
#from nltk.tokenize import StanfordTokenizer

@app.route('/')
def show_entries():
    # the the latest text from database
    m = db.session.query(db.func.max(models.Entry.id).label("max_id")).one()
    txt = db.session.query(models.Entry).get(m.max_id)
    
    print "txt: ", str(txt)
    _txt = str(txt).split('\'')
    _input = _txt[1].split('@')
    entries = _input[0]
    print "entries: ", entries

    global words
    if len(_input[1]) > 0:
        words = _input[1].split(',')
        print "words: ", words
        #print "words-tye: ", type(words)
    
    #outputs = entries
    s_outputs = {}
    s1_output = {}
    s2_output = {}
    s1_child_output = {}
    s2_child_output = {}
    s1 = ""
    s2 = ""
    s1_child = ""
    s2_child = ""
    
    if len(entries) > 0: #Syntactic simplification firstly
        #print "entries-:", entries
        #tokens = StanfordTokenizer().tokenize(entries)
        _syn_ret = dt_sent.simp_syn_sent(entries)
        #BUG here, todo
        if len(_syn_ret)>0:
            #print "S1"            
            (s1, s1_child, s2, s2_child, syn_ret) = dt_sent._get_split_ret(_syn_ret)
            
            if len(syn_ret) > 0: # there is the child - 3 layers
                #outputs = utils.wordcal.check_word_(syn_ret, words)
                #s_outputs = wordcal.check_word(_syn_ret, words)

                if len(s1_child) > 0:
                    s1_output = wordcal.check_word(s1, words)
                    s1_child_output = wordcal.check_word(s1_child, words)
                else:
                    s1_output = wordcal.check_word(s1, words)

                if len(s2_child) > 0: 
                    s2_output = wordcal.check_word(s2, words) 
                    s2_child_output = wordcal.check_word(s2_child, words) 
                else:
                    s2_output = wordcal.check_word(s2, words)
        
        s_outputs = wordcal.check_word(entries, words)          
    
    print "s1_output: ", s1_output
    print "s1_child_output: ", s1_child_output
    print "s2_output: ", s2_output
    print "s2_child_output: ", s2_child_output
    print "s_outputs: ", s_outputs

    return render_template('show_entries.html', entries=entries, s_outputs=s_outputs, s1_child=s1_child, s1_child_output=s1_child_output, s1_output=s1_output, s2_child=s2_child, s2_child_output=s2_child_output, s2_output=s2_output)


# this view let the user add new entries if they are logged in
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    txt = request.form['input']
    wordlist = request.form['words']
    #_wordlist = request.form['words']
    #print "wordlist: ", _wordlist
    #print 'txt: ', txt
    #print "wordlist: ", wordlist
    db.session.add(models.Entry(txt, wordlist))
    db.session.commit()

    flash('New entry was successfully posted')

    #return render_template('show_entries.html', entries=entries)
    return redirect(url_for('show_entries'))


#login and logout
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='144.214.20.231',debug=True)
