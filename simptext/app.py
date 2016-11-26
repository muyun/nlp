# -*- coding: utf-8 -*-
"""
 Logical Model - controller

 @author wenlong
"""
import os

from flask import Flask, request, render_template, session, g, redirect, url_for, abort, \
    render_template, flash, jsonify

from flask_sqlalchemy import SQLAlchemy

from forms import EntryForm, SelectForm

import json

import time

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# this model is the db model
import models

#from algs import simp
from simptext import dt_sent, wordcal
#import simptext

#word_start = time.time()
word1 = dt_sent.read_xlsx_file('./simptext/dataset/wordlist.xlsx', 1, 1)
word2 = dt_sent.read_xlsx_file('./simptext/dataset/wordlist.xlsx', 2, 1)
word3 = dt_sent.read_xlsx_file('./simptext/dataset/wordlist.xlsx', 3, 1)
word4 = dt_sent.read_xlsx_file('./simptext/dataset/wordlist.xlsx', 4, 1)
word_end = time.time()

#word_during = word_end - word_start
#print "word_during: ", word_during
#words = dt_sent.get_edblist('simptext/dataset/EDB_List.txt')
#from nltk.tokenize import StanfordTokenizer

#@app.route('/show_entries')
def show_entries():
    #form = EntryForm()
    # the the latest text from database
    m = db.session.query(db.func.max(models.Entry.id).label("max_id")).one()
    #txt = str(db.session.query(models.Entry).get(m.max_id))
    etxt = models.Entry.query.get(m.max_id)
    #se = str(etxt).split('@') 
    #entries = str(se[0])  
    #print "entries: ", entries
    #print "txt: ", str(e[0])
    
    #ret = ""
    #s = db.session.query(db.func.max(models.Setting.id).label("max_id")).one()
    #ret = str(db.session.query(models.Setting).get(s.max_id))
    #print "setting: ", ret

    #s = db.session.query(db.func.max(models.Select.id).label("max_id")).one()
    #txt = str(db.session.query(models.Entry).get(m.max_id))
    #stxt = models.Select.query.get(s.max_id)

    #import pdb; pdb.set_trace()
    words = []
    global word1, word2, word3, word4
    #_txt = str(txt).split('\'')
    se = str(etxt).split('@')
    entries = str(se[0])
    wordlist = str(se[1])
    wordlevel = str(se[2])
    print "se2: ", str(se[3])
    algs = range(1,10)
    if len(str(se[3])) > 0:
        algs = [int(i) for i in str(se[3]).split()]    
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

        s_outputs = wordcal.check_word(entries, words)   

        begin_time5 = time.time() - begin_time4
        print "The time of wordcal function: ", begin_time5
        
    print "s1_output: ", s1_output
    print "s2_output: ", s2_output
    print "s_outputs: ", s_outputs

    return render_template('show_entries.html', form=form, entries=entries, s_outputs=s_outputs, s1_output=s1_output, s2_output=s2_output)
    #return render_template('show_entries.html', form=form, wordlist=wordlist, entries=entries, s_outputs=s_outputs, s1_child=s1_child, s1_child_output=s1_child_output, s1_output=s1_output, s2_child=s2_child, s2_child_output=s2_child_output, s2_output=s2_output)


# this view let the user add new entries if they are logged in
@app.route('/', methods=['GET','POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    form = EntryForm()
    txt = request.form['input']
    print "input: ", txt
    #
    #words = ""
    wordinput = request.form['wordinput']
    #words = form.words.data
    print "words: ", wordinput
    #wordlevel = ""
    #wordlevel = request.form['wordlevel']
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
    db.session.add(models.Entry(txt, wordinput, wordlevel, alg))

    #sform = SelectForm()
    #txt = request.sform['input']
    #db.session.add(models.Select(words, wordlevel, alg))
    db.session.commit()

    flash('New entry was successfully posted')

    #return render_template('show_entries.html')
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
