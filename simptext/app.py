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

from forms import EntryForm, ParamForm

import json

import time

from nltk.corpus import wordnet as wn

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
word5 = wordcal.get_words('./simptext/dataset/basic.txt')
word6 = wordcal.get_words('./simptext/dataset/cet4.txt')
word7 = wordcal.get_words('./simptext/dataset/cet6.txt') + word6

#word_end = time.time()

#word_during = word_end - word_start
#print "word_during: ", word_during
#words = dt_sent.get_edblist('simptext/dataset/EDB_List.txt')
from nltk.tokenize import StanfordTokenizer
endings = ['.', '!', '?']

from string import capwords

import enchant
d = enchant.Dict("en_US")

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

def get_definition(soutput):
    result = []
    for item in soutput: 
        #import pdb; pdb.set_trace()
        if isinstance(item, dict):
            res = {}
            #import pdb; pdb.set_trace()
            k = item.keys()[0]
            if len(item.values()) == 1 and len(wn.synsets(k)) > 0:
                res[k] = wn.synsets(k)[0].definition()
                result.append(res)
    return result

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
    flag = ""

    #print "algs-", request.form.getlist('algs')
    #print "level-", request.form.getlist('wordlevel')
    ending = "" # check the ending of the entries

    global word1, word2, word3, word4, word5, word6, word7
    words = []
    #words = []
    if len(etxt) > 0:
        #print "etxt: ", etxt[0]
    
        db.execute('delete from entries where id = (SELECT MAX(id) FROM entries);')
        #db.commit()
        #
        #db = get_db()
        pcur = db.execute('select * from params WHERE id = (SELECT MAX(id) FROM params);')
        ptxt = pcur.fetchall();

        #db.execute('delete from params where id = (SELECT MAX(id) FROM params);')
        db.commit()

        #print "ptxt_init_:", ptxt
        wordlist = ""
        if len(ptxt) > 0:
            wordlist = str(ptxt[0][1])
            #print "_wordlist:", wordlist

        #words = []
        #global word1, word2, word3, word4
        #_txt = str(txt).split('\'')
        #se = str(etxt[0]).split(',')
        entries = str(etxt[0][1])
        #wordlist = str(etxt[0][2])
        wordlevel = str(etxt[0][3])
        print "se2: ", str(etxt[0][4])
        algs = []
        if len(str(etxt[0][4])) > 0:
            algs = [int(i) for i in str(etxt[0][4]).split()]    
    #form.algs.choices =  ''.join(str(e) for e in algs)

        print "entries: ", entries
        #print "wordlist: ", wordlist
        print "wordlevel: ", wordlevel
        print "algs: ", algs

        if len(wordlist) == 0:
            if int(wordlevel) == 1:
    	        words = word1
            if int(wordlevel) == 2:
    	        words = word2
            if int(wordlevel) == 3:
    	        words = word3	
    	    if int(wordlevel) == 4:
    	        words = word4
            if int(wordlevel) == 5:
                words = word5
            if int(wordlevel) == 6:
                words = word6
            if int(wordlevel) == 7:
                words = word7 
            if int(wordlevel) == 0:
            	#error = 'Please include at least one word in the wordlist'
                flag = "flag"

        #import pdb; pdb.set_trace()  
        if len(wordlist) > 0 and len(words) != 4496 and len(words) != 1918 and len(words) != 1002 and len(words) != 3257: # word4 by default
            words = []    
    	    for w in wordlist.split(','):
    		w = w.strip()
    		words.append(w)
        
        #if len(wordlist) > 0:
        #    words = wordlist.split(',')
            #import pdb; pdb.set_trace()
        
    words = list(set(words))
    #import pdb; pdb.set_trace()
    print "words:", words
    """ 
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
    """
        #import pdb; pdb.set_trace()
    if len(words) == 0:
        words= word4
    
    print "flag: ", flag

    #import pdb; pdb.set_trace()
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

    #import pdb; pdb.set_trace()
    begin_time1 = time.time()
    #if len(entries) >0 :
    #    s_outputs = wordcal.check_word(entries, words)

    if len(entries) == 0:
        s_outputs = {}
  
    elif len(entries) > 1 and d.check(entries[1]) and len(algs) > 0 and len(flag) == 0: #Syntactic simplification firstly
        #print "entries-:", entries
        #tokens = StanfordTokenizer().tokenize(entries)
        entries_list =   StanfordTokenizer().tokenize(entries)
        #ending = ""
        if entries_list[-1] not in endings:
            entries_list.append('.')
        elif entries_list[-1] == '!':
            ending = '!'
            entries_list[-1] = '.'
        elif entries_list[-1] == '?':
            ending = '?'
            entries_list[-1] = '.'
        else:
            pass
        _entries = ' '.join(entries_list)

        begin_time2 = time.time()

        _syn_ret, alg1 = dt_sent.simp_syn_sent(entries, algs)
        #BUG here, todo
        """
        if len(_syn_ret) > 0:
            (s1, s2) = dt_sent.get_split_ret(_syn_ret)

            if len(s2) > 0:
            #begin_time4 = time.time()
                outputs = wordcal.check_word(s1+s2, words)
                print "output: ", s1_output
                stop_index = outputs.index('.')
                s1_output = outputs[0:stop_index+1]
                s2_output = outputs[stop_index+1:]
                #s2_output = wordcal.check_word(s2, words)
                #s3_output = wordcal.check_word(s1, words)
            else:
            	s1_output = wordcal.check_word(s1, words)
        """
        #import pdb; pdb.set_trace()
        s_outputs = wordcal.check_word(entries, words)
        if len(_syn_ret) > 0:
            (s1, s1_child, s2, s2_child, ret, alg2) = dt_sent._get_split_ret(_syn_ret, algs)

            split_time = time.time() - begin_time2
            print "The time of split function: ", split_time

            begin_time3 = time.time()
            #s_tags = wordcal.get_pos(entries)
            s_outputs = wordcal.check_word(entries, words)  
            referenced = []

            #import pdb; pdb.set_trace()
            if len(ret) > 0: # there is the child: 3 layer
                if int(wordlevel) != 5:
                #import pdb; pdb.set_trace()         
                    if(s1_child) > 0:
                        #s1_child_output = wordcal.check_word(s1_child, words)
                        s1_child_output, referenced = wordcal.get_word_candidates(s1_child, s_outputs, referenced)
                    #s1_output = wordcal.check_word(s1, words)
                    s1_output,referenced = wordcal.get_word_candidates(s1, s_outputs, referenced)
                
                    if (s2_child) > 0:
                        #s2_child_output = wordcal.check_word(s2_child, words)
                        s2_child_output,referenced = wordcal.get_word_candidates(s2_child, s_outputs,referenced)
                #import pdb; pdb.set_trace()
                    #s2_output = wordcal.check_word(s2, words)
                    s2_output,referenced = wordcal.get_word_candidates(s2, s_outputs,referenced)

                """
                if int(wordlevel) == 5:
                    if (s1_child) > 0:
                        s1_child_output = unicode(s1_child).split()
                    s1_output = unicode(s1).split()

                    if (s2_child) >0:
                        s2_child_output = unicode(s1_child).split()
                    s2_output = unicode(s1).split()
                """

            wordcal_time = time.time() - begin_time3
            print "The time of wordcal function: ", wordcal_time

    elif len(entries) > 1 and len(algs) == 0: # not english words
        #s_outputs = unicode(entries)
        if not d.check(entries[1]): # not english words
            s_outputs = unicode(entries)
        else:
            s_outputs = entries.split()
    #elif len(entries) > 1:
    #    s_outputs = wordcal.check_word(entries, words)
    else:
        pass

    #print "words:", words
    #_words = '\r\n'.join(x for x in words)
    #_words =   list(set(words))
    begin_words_sort_time = time.time()
    words.sort(key = lambda k : k.lower()) 
    _words = '\r\n'.join(x for x in words)
    end_words_sort_time = time.time() 
    print "The time of word sort function: ", end_words_sort_time - begin_words_sort_time
    
    all_time = time.time() - begin_time1
    print "The time of all functions: ", all_time

    print "s1_output: ", s1_output
    print "s1_child_output: ", s1_child_output
    print "s2_output: ", s2_output
    print "s2_child_output: ", s2_child_output
    print "s_outputs: ", s_outputs


    # get the definiton of the 
    sdefinition= {}
    sdefinition = get_definition(s_outputs)
    print "sdefinition: ", sdefinition
    #import pdb; pdb.set_trace()
     
    #return render_template('show_entries.html', form=form, entries=entries, s_outputs=s_outputs, s1_output=s1_output, s2_output=s2_output, flag=flag)
    return render_template('show_entries.html', form=form, words=_words, entries=entries, sdefinition=sdefinition, s_outputs=s_outputs, s1_child=s1_child, s1_child_output=s1_child_output, s1_output=s1_output, s2_child=s2_child, s2_child_output=s2_child_output, s2_output=s2_output, flag=flag)
    #return render_template('show_entries.html', form=form)

@app.route('/print', methods=['GET','POST'])
def print_words():
    error = None
    db = get_db()
    #cur = db.execute('select * from params WHERE id = (SELECT MAX(id) FROM params);')
    #etxt = cur.fetchall();
    #level = request.args.get('wordlevel', 4, type=int);

    pcur = db.execute('select * from params WHERE id = (SELECT MAX(id) FROM params);')
    etxt = pcur.fetchall();
    db.commit()

    words = []
    #etxt = "test"
    #print "etxt_init: ", etxt
    if len(etxt) == 0:
        #print "etxt: ", etxt
        #print "etxt[0]: ", etxt[0]
        error = "Please submit the input firstly."

    global word1, word2, word3, word4, word5, word6, word7
    if len(etxt) > 0:
        #print "etxt_print: ", etxt
        #se = str(etxt[0]).split(',')
        #entries = str(etxt[0][1])
        #wordlist = str(etxt[0][2])
        level = str(etxt[0][2])

        if not level:
        	level = "4"
        print "wordlevel_print: ", level
        #level = 1 

        #print "wordlist: ", wordlist
        #print "wordlevel: ", wordlevel

        if int(level) == 1:
            words = word1
        if int(level) == 2:
            words = word2
        if int(level) == 3:
            words = word3 
        if int(level) == 4:
            words = word4
        if int(level) == 5:
            words = word5
        if int(level) == 6:
            words = word6
        if int(level) == 7:
            words = word7
        if int(level) == 0:
            error = "No words in this level."

    #print "words:", words
    #import pdb; pdb.set_trace()
    _words = '\r\n'.join(x for x in words)
    #print "_words:", _words

    #return redirect(url_for('show_entries'))
    return render_template('print_words.html', words=_words, error=error)


@app.route('/_submit_level')
def submit_level():
    #error = None
    #db = get_db()

    wordinput = ""
    alg = ""
    level = json.loads(request.args.get('wordlevel'))
    #wordlevel = json.loads(request.args.get('wordlevel'));
    print "wordlevel_init: ", level
    #print "wordlevel:", wordlevel
    #db.execute('insert into params (words, level, algs) values (?, ?, ?)', [wordinput, level, alg])
    #db.commit()
    """
    words = []
    
    etxt = "test"
    global word1, word2, word3, word4
    if len(etxt):
        print "etxt-: ", etxt
        #se = str(etxt[0]).split(',')
        #entries = str(etxt[0][1])
        #wordlist = str(etxt[0][2])
        #wordlevel = 
        print "wordlevel-: ", wordlevel
        #wordlevel = 1 

        #print "wordlist: ", wordlist
        #print "wordlevel: ", wordlevel

        if int(wordlevel) == 1:
            words = word1
        if int(wordlevel) == 2:
            words = word2
        if int(wordlevel) == 3:
            words = word3   
        if int(wordlevel) == 4:
            words = word4
        if int(wordlevel) == 0:
            error = "No words in this level."
    """
    #print "words:", words
    #return jsonify(result=words)
    return jsonify(result=level)
    #return redirect(url_for('show_entries'))
    #return redirect(url_for('print_words'))
    #return render_template('print_words.html', words=words, error=error)

@app.route('/submit_words', methods=['GET','POST'])
def submit_words():
    #
    form = ParamForm()

    wordinput = str(request.form['words']).split(",")

    #wordlevel = ""
    #wordlevel = json.loads(request.args.get('wordlevel'))
    #wordlevel = ""
    alg = ""

    _wordinput = ",".join(x for x in wordinput)
    #global word1, word2, word3, word4
    #_wordinput = word4
    #wordlevel = json.loads(request.args.get('wordlevel'));
    #print "wordinput: ", wordinput
    #print "_wordinput: ", _wordinput
    #print "wordlevel:", wordlevel
    db = get_db()
    #db.execute('insert into params (words, level, algs) values (?, ?, ?)', [_wordinput, wordlevel, alg])
    db.execute('update params set words=? WHERE id = (SELECT MAX(id) FROM params)', [_wordinput])
    #db.commit()    

    #db = get_db()
    #pcur = db.execute('select * from params WHERE id = (SELECT MAX(id) FROM params);')
    #ptxt = pcur.fetchall();
    db.commit()

    """
    print "ptxt_init:", ptxt
    
    wordlist = ""
    if len(ptxt) > 0:
        wordlist = str(ptxt[0][1])
        print "wordlist_init:", wordlist
    """
    
    #return jsonify(result=wordinput)
    return redirect(url_for('show_entries'))


@app.route("/test" , methods=['GET', 'POST'])
def test():
    #form = EntryForm()
    #select = request.args.get('wordlevel')
    select = request.values.get("wordlevel")
    #select = request.form.get('wordlevel')
    print "select:", str(select)
    return(str(select)) # just to see what select is


def get_words(inputs):
    vocabulary_opinion = int(request.form['vocabulary'])
    print "vocabulary_opinion:", vocabulary_opinion
    
    wordlevel = ""
    if vocabulary_opinion == 0:
        wordlevel = "4"
    if vocabulary_opinion == 1:
        wordlevel = request.form['wordlevel']
    #form.process()
    #wordlevel = form.wordlevel.data
    print "wordlevel_init: ", wordlevel
    #txt = form.input.data
    #words = form.wordinput.data
    #wordlevel = form.wordlevel.data
 
    words = []
    global word1, word2, word3, word4, word5, word6, word7
    if int(wordlevel) == 1:
        words = word1
    if int(wordlevel) == 2:
        words = word2
    if int(wordlevel) == 3:
        words = word3   
    if int(wordlevel) == 4:
        words = word4
    if int(wordlevel) == 5:
        words = word5
    if int(wordlevel) == 6:
        words = word6
    if int(wordlevel) == 7:
        words = word7       
    if int(wordlevel) == 0:
        error = "No words in this level."

    wordinput = ""
    if vocabulary_opinion == 1:
        _wordinput = str(request.form['words']).split(",")
        #wordinput_ = list(set(_wordinput+words))
        wordinput_ = list(set(_wordinput))
        wordinput = ",".join(x for x in wordinput_)
        print "wordinput_int: ", _wordinput

    if vocabulary_opinion == 0:
        wordinput = ",".join(x for x in words)

    #print "wordlevel:", wordlevel
    #db = get_db()
    #db.execute('insert into params (words, level, algs) values (?, ?, ?)', [_wordinput, wordlevel, alg])
    #db.execute('update params set words=? WHERE id = (SELECT MAX(id) FROM params)', [wordinput])
    #db.commit()

    return wordinput, wordlevel


def get_sentences():
    #wordinput = ""
    #print "wordinput: ", wordinput
    #
    #words = ""
    #wordinput = ""
    #algs0 = form.algs.data
    #print "algs0: ", algs0 
    #selected_sent = request.form.getlist('cselect')
    #if not selected_sent:
    #print "selected_sent:", selected_sent
    sentence_opinion = int(request.form['sentence'])
    print "sentence_opinion:", sentence_opinion
    _algs = []
    if sentence_opinion == 0:
        _algs = [u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9', u'10']
    if sentence_opinion == 1:
        _algs = form.algs.data
        
    print "algs_init:", _algs

    alg = ""
    alg = ' '.join(str(e) for e in _algs)
    print "alg_init: ", alg
    #wordlist = ""
    #_wordlist = request.form['words']
    #txt = form.input.data
    s1 = ""
    s2 = ""

    return alg, s1, s2


# this view let the user add new entries if they are logged in
@app.route('/add', methods=['GET','POST'])
def add_entry():
    form = EntryForm()
    inputs = ""
    inputs = request.form['input']
    print "input_init: ", inputs
    #if not session.get('logged_in'):
    #    abort(401)

    #_wordinput = request.form['wordinput']
    #words = form.words.data
    #global word1, word2, word3, word4
    #wordinput = ",".join(x for x in word4)
    #wordinput = ""
    #print "_wordinput_init: ", wordinput
    #wordlevel = ""
    #wordlevel = request.form['wordlevel']
    #wordlevel = "4"
    #form.wordlevel.default = 4
    #print "wordlevel0: ", wordlevel
    global word4

    cselect = request.form.getlist('cselect')
    #if not selected_voc:
    print "cselect:", cselect
    if len(cselect) == 0:
        print "There is no selection"
    if len(cselect) == 1:
        if int(cselect[0]) == 1: # vocabulary
            wordinput, wordlevel = get_words(inputs)
            db = get_db()    
            #db.execute('insert into params (words, level, algs) values (?, ?, ?)', [_wordinput, wordlevel, alg])
            db.execute('update params set words=? WHERE id = (SELECT MAX(id) FROM params)', [wordinput])
            db.execute('insert into entries (inputs, words, level, algs, s1, s2) values (?, ?, ?, ?, ?, ?)',
               [inputs, wordinput, wordlevel, "", "", ""])
            db.commit()

        if int(cselect[0]) == 2: # sentence
            alg, s1, s2 = get_sentences()
            wordinput = ",".join(x for x in word4)

            db = get_db()
            db.execute('insert into entries (inputs, words, level, algs, s1, s2) values (?, ?, ?, ?, ?, ?)',
               [inputs, wordinput, "4", alg, s1, s2])

            #db.execute('update params set level=? WHERE id = (SELECT MAX(id) FROM params)', [wordlevel])
            #db.execute('update params set words=? WHERE id = (SELECT MAX(id) FROM params)', [wordinput])
            db.commit()

    if len(cselect) == 2:
        wordinput, wordlevel = get_words(inputs)
        alg, s1, s2 = get_sentences()

        db = get_db()
        db.execute('insert into entries (inputs, words, level, algs, s1, s2) values (?, ?, ?, ?, ?, ?)',
               [inputs, wordinput, wordlevel, alg, s1, s2])

        db.execute('update params set level=? WHERE id = (SELECT MAX(id) FROM params)', [wordlevel])
        db.execute('update params set words=? WHERE id = (SELECT MAX(id) FROM params)', [wordinput])
        db.commit()

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

    form = paramForm()
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
    app.run(debug=True)
    #app.run(host='144.214.20.231',port = 5001,debug=True, threaded=True)
    #app.run(host='144.214.20.231',debug=True, threaded=True)
