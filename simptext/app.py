# -*- coding: utf-8 -*-
"""
 Logical Model - controller

 @author wenlong
"""
import os

from flask import Flask, request, render_template, session, g, redirect, url_for, abort, \
    render_template, flash, jsonify

from flask_sqlalchemy import SQLAlchemy

from forms import SelectForm, EntryForm

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

word1 = dt_sent.read_xlsx_file('./simptext/dataset/wordlist.xlsx', 1, 1)
word2 = dt_sent.read_xlsx_file('./simptext/dataset/wordlist.xlsx', 2, 1)
word3 = dt_sent.read_xlsx_file('./simptext/dataset/wordlist.xlsx', 3, 1)
word4 = dt_sent.read_xlsx_file('./simptext/dataset/wordlist.xlsx', 4, 1)
#words = dt_sent.get_edblist('simptext/dataset/EDB_List.txt')
#from nltk.tokenize import StanfordTokenizer

@app.route('/')
def show_entries():
    form = EntryForm()
    # the the latest text from database
    entries = ""
    m = db.session.query(db.func.max(models.Entry.id).label("max_id")).one()
    #txt = str(db.session.query(models.Entry).get(m.max_id))
    txt = models.Entry.query.get(m.max_id)
    
    entries = str(txt)   
    print "entries: ", entries

    #ret = ""
    #s = db.session.query(db.func.max(models.Setting.id).label("max_id")).one()
    #ret = str(db.session.query(models.Setting).get(s.max_id))
    #print "setting: ", ret

    words = []
    global word1, word2, word3, word4
    #_txt = str(txt).split('\'')
    se = str(txt).split('@')
    entries = str(se[0])
    wordlist = str(se[1])
    wordlevel = str(se[2])
    #algs = str(se[2])

    print "wordlist: ", wordlist
    print "wordlevel: ", wordlevel
    #print "algs: ", algs
    
    if len(wordlist) > 0:
    	for w in wordlist.split(','):
    		w = w.strip()
    		words.append(w)
        #words = wordlist.split(',')
        #print "words: ", words
            #print "words-tye: ", type(words)
            #wordlevel = 0
    else:
    	if int(wordlevel) == 1:
    		words = word1
        if int(wordlevel) == 2:
    		words = word2
        if int(wordlevel) == 3:
    		words = word3	
    	if int(wordlevel) == 4:
    		words = word4	
    
    #print "words: ", words
    # TODO: update the ALGs
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
        _syn_ret, alg1 = dt_sent.simp_syn_sent(entries)
        #BUG here, todo
        if len(_syn_ret) > 0:
            #print "S1"            
            (s1, s1_child, s2, s2_child, syn_ret, algs) = dt_sent._get_split_ret(_syn_ret)
            
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

    return render_template('show_entries.html', form=form, entries=entries, s_outputs=s_outputs, s1_child=s1_child, s1_child_output=s1_child_output, s1_output=s1_output, s2_child=s2_child, s2_child_output=s2_child_output, s2_output=s2_output)


# this view let the user add new entries if they are logged in
@app.route('/add', methods=['GET','POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    txt = request.form['input']
    print "input: ", txt
    words = request.form['wordinput']
    wordlevel = request.form['wordlevel']
    #wordlist = ""
    #_wordlist = request.form['words']
    #print "wordlist: ", _wordlist
    #print 'txt: ', txt
    #print "wordlist: ", wordlist
    db.session.add(models.Entry(txt, words, wordlevel))
    db.session.commit()

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
    wordinput = ""
    if request.method == 'POST':
    	"""
        if form.validate() == False:
            flash('All fields are required. ')
            return render_template('setting.html', form = form)
        else:
        """
        #if form.validate_on_submit():
        #wordlist = form['words']
        #edblist = form['edblist']
        #algs = form['algs']
        #words = form.wordinput.data
        words = ""
        #wordlevel = form.wordlevel.data
        wordlevel = ""
        algs = ' '.join(str(e) for e in form.algs.data)
        #print "wordinput: ", words
        #print "wordlist: ", form.wordlist.data
        #print "wordlevel: ", wordlevel
        print "algs: ", algs

        db.session.add(models.Setting(words, wordlevel, algs))
        db.session.commit()
            
        return redirect(url_for('show_entries'))

    return render_template('setting.html', form = form)


if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='144.214.20.231',debug=True)
