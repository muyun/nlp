# -*- coding: utf-8 -*-
"""
 Logical Model - controller

 @author wenlong
"""
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, render_template, session, g, redirect, url_for, abort, \
    render_template, flash, jsonify

from flask_sqlalchemy import SQLAlchemy

from forms import EntryForm, SelectForm

import json

import time

app = Flask(__name__)
app.config.from_object(__name__)
#app.config.from_object('config.DevelopmentConfig')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)
# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'simptext.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='admin'
))
#app.config.from_envvar('simptext_SETTINGS', silent=True)

# this model is the db model
#import models

#from algs import simp
from simptext import dt_sent, wordcal
#import simptext

#word_start = time.time()
word1 = dt_sent.read_xlsx_file('./simptext/dataset/wordlist.xlsx', 1, 1)
word2 = dt_sent.read_xlsx_file('./simptext/dataset/wordlist.xlsx', 2, 1)
word3 = dt_sent.read_xlsx_file('./simptext/dataset/wordlist.xlsx', 3, 1)
word4 = dt_sent.read_xlsx_file('./simptext/dataset/wordlist.xlsx', 4, 1)
#word_end = time.time()

#word_during = word_end - word_start
#print "word_during: ", word_during
#words = dt_sent.get_edblist('simptext/dataset/EDB_List.txt')
#from nltk.tokenize import StanfordTokenizer

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def show_entries():
    form = EntryForm()
    # the the latest text from database
    #m = db.session.query(db.func.max(models.Entry.id).label("max_id")).one()
    #txt = str(db.session.query(models.Entry).get(m.max_id))
    #etxt = db.session.query.get(m.max_id)
    #etxt = models.Entry.query.get(m.max_id)
    db = get_db()
    cur = db.execute('select * from entries WHERE id = (SELECT MAX(id) FROM entries);')
    etxt = cur.fetchall();
    if len(etxt) == 0:
    	entries = ""
    if len(etxt) > 0:
        print "etxt: ", etxt[0]
    
        db.execute('delete from entries where id = (SELECT MAX(id) FROM entries);')
        db.commit()

        #import pdb; pdb.set_trace()
        words = []
        global word1, word2, word3, word4
        #_txt = str(txt).split('\'')
        #se = str(etxt[0]).split(',')
        entries = str(etxt[0][1])
        wordlist = str(etxt[0][2])
        wordlevel = str(etxt[0][3])
        print "se2: ", str(etxt[0][4])
        algs = range(1,10)
        if len(str(etxt[0][4])) > 0:
            algs = [int(i) for i in str(etxt[0][4]).split()]    
    #form.algs.choices =  ''.join(str(e) for e in algs)

        print "entries: ", entries
        print "wordlist: ", wordlist
        print "wordlevel: ", wordlevel
        print "algs: ", algs
    
        if len(wordlist) > 0:
            _words = []
    	    for w in wordlist.split(','):
    		    w = w.strip()
    		    _words.append(w)

            if int(wordlevel) == 0:
                words = _words
            else:
                if int(wordlevel) == 1:
                    words = list(_words) + list(word1)
                if int(wordlevel) == 2:
                    words = list(_words) + list(word2)
                if int(wordlevel) == 3:
                    words = list(_words) + list(word3)   
                if int(wordlevel) == 4:
                    words = list(_words) + list(word4)
                    #print "words4: ", words
        elif len(wordlevel) > 0:
    	    if int(wordlevel) == 1:
    		    words = word1
            if int(wordlevel) == 2:
    		    words = word2
            if int(wordlevel) == 3:
    		    words = word3	
    	    if int(wordlevel) == 4:
    		    words = word4
        else:
            pass	

    #print "words: ", words
    #print "words: ", words
    # TODO: update the ALGs
    #outputs = entries

    s_outputs = {}
    s1_output = {}
    s2_output = {}
    s1 = ""
    s2 = ""

    """
    if len(entries) == 0:
    	s1 = str(etxt[0][5])
    	s2 = str(etxt[0][6])
    	print "s1: ", s1
    	print "s2: ", s2
    	s1_output = wordcal.check_word(s1, words)
        s2_output = wordcal.check_word(s2, words)
    """
        #s_outputs = wordcal.check_word(entries, words)
       
    if len(entries) > 0: #Syntactic simplification firstly
        #print "entries-:", entries
        #tokens = StanfordTokenizer().tokenize(entries)
        _syn_ret, alg1 = dt_sent.simp_syn_sent(entries, algs)
        #BUG here, todo
        
        if len(_syn_ret) > 0:
            (s1, s2) = dt_sent.get_split_ret(_syn_ret)

            begin_time4 = time.time()
            s1_output = wordcal.check_word(s1, words)
            s2_output = wordcal.check_word(s2, words)

        begin_time4 = time.time()
        s_outputs = wordcal.check_word(entries, words)   

        begin_time5 = time.time() - begin_time4
        print "The time of wordcal function: ", begin_time5
        
    print "s1_output: ", s1_output
    print "s2_output: ", s2_output
    print "s_outputs: ", s_outputs
    
    return render_template('show_entries.html', form=form, entries=entries, s_outputs=s_outputs, s1_output=s1_output, s2_output=s2_output)
    #return render_template('show_entries.html', form=form, wordlist=wordlist, entries=entries, s_outputs=s_outputs, s1_child=s1_child, s1_child_output=s1_child_output, s1_output=s1_output, s2_child=s2_child, s2_child_output=s2_child_output, s2_output=s2_output)
    #return render_template('show_entries.html', form=form)

# this view let the user add new entries if they are logged in
@app.route('/add', methods=['GET','POST'])
def add_entry():
    #if not session.get('logged_in'):
    #    abort(401)

    form = EntryForm()
    inputs = ""
    inputs = request.form['input']
    print "input: ", inputs
    #
    #words = ""
    wordinput = ""
    wordinput = request.form['wordinput']
    #words = form.words.data
    print "words: ", wordinput
    #wordlevel = ""
    #wordlevel = request.form['wordlevel']
    wordlevel = ""
    wordlevel = request.form['wordlevel']
    #wordlevel = form.wordlevel.data
    print "wordlevel: ", wordlevel
    #txt = form.input.data
    #words = form.wordinput.data
    #wordlevel = form.wordlevel.data
    
    #algs0 = form.algs.data
    #print "algs0: ", algs0
    alg = ' '.join(str(e) for e in form.algs.data)
    #wordlist = ""
    #_wordlist = request.form['words']
    #txt = form.input.data
    s1 = ""
    s2 = ""

    #db.session.add(models.Entry(txt, wordinput, wordlevel, alg, s1, s2))
    #db.session.commit()
    db = get_db()
    db.execute('insert into entries (inputs, words, level, algs, s1, s2) values (?, ?, ?, ?, ?, ?)',
               [request.form['input'], request.form['wordinput'], request.form['wordlevel'],
               alg, s1, s2])
    db.commit()

    flash('New entry was successfully posted')

    #return render_template('show_entries.html', text=text)
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
            #return redirect(url_for('show_entries'))
            return redirect(url_for('add_entry'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    #return redirect(url_for('show_entries'))
    return redirect(url_for('login'))

@app.route('/setting', methods=['GET', 'POST'])
def setting():
    if not session.get('logged_in'):
        abort(401)

    form = SelectForm()
    words = request.form['words']
    wordlevel = request.form['wordlevel']
 
    #algs0 = form.algs.data
    #print "algs0: ", algs0
    alg = ' '.join(str(e) for e in form.algs.data)

    db.session.add(models.Select(words, wordlevel, alg))
    db.session.commit()

    #flash('New setting was successfully posted')
         
    return redirect(url_for('show_entries'))

    #return render_template('setting.html', form = form)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
    #app.run(host='144.214.20.231',port = 5001,debug=True)
