# -*- coding: utf-8 -*-
"""
 Logical Model

 @author wenlong
"""
import os

from flask import Flask, request, render_template, session, g, redirect, url_for, abort, \
    render_template, flash, jsonify

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import models

import utils.dt, utils.cal, utils.alg

words = utils.dt.read_xlsx_file('./dataset/wordlist.xlsx', 1)
#from nltk.tokenize import StanfordTokenizer

@app.route('/')
def show_entries():
    # the the latest text from database
    m = db.session.query(db.func.max(models.Entry.id).label("max_id")).one()
    txt = db.session.query(models.Entry).get(m.max_id)
    entries = str(txt.text)
    print "entries: ", entries

    #outputs = entries
    outputs = {}
     
    if len(entries) > 0: #Syntactic simplification firstly
        #tokens = StanfordTokenizer().tokenize(entries)
        syn_ret = utils.alg.simp_syn_sent(entries)
        #print "Syntactic result: ", syn_ret
        if len(syn_ret) > 0: # next simplify the word
            outputs = utils.cal.check_word(syn_ret, words)
                  
    print "output: ", outputs

    return render_template('show_entries.html', entries=entries , outputs=outputs )


# this view let the user add new entries if they are logged in
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    txt = request.form['input']
    #print 'txt: ', txt
    db.session.add(models.Entry(txt))
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
