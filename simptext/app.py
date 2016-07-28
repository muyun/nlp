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

@app.route('/')
def show_entries():
    # the the latest text from database
    m = db.session.query(db.func.max(models.Entry.id).label("max_id")).one()
    txt = db.session.query(models.Entry).get(m.max_id)
    entries = str(txt.text)
    print "entries: ", entries

    #Syntactic simplification
    coordi = utils.alg.simp_coordi_sent(entries)
    print "simp_sent: ", coordi

    #outputs = entries
    outputs = utils.cal.check_word(coordi, words)
    # simplify the words in this text  
    if len(coordi) > 0:
        outputs = utils.cal.check_word(coordi, words)
        #outputs = coordi
        #break
    else:
        # subordi
        subordi = utils.alg.simp_subordi_sent(entries)
        if len(subordi) > 0:
            outputs = utils.cal.check_word(subordi, words)
            #outputs = coordi
            #break
        else: #advcl
            advcl = utils.alg.simp_advcl_sent(entries)
            if len(advcl) > 0:
                outputs = utils.cal.check_word(advcl, words)

                #break
            else: #parti 
                      
                parti = utils.alg.simp_parti_sent(str(entries))
                if len(parti) > 0:
                    outputs = utils.cal.check_word(parti, words)
                    #break
                else: #adjec   
                    adjec = utils.alg.simp_adjec_sent(str(entries)) 
                    if len(adjec) > 0:
                        outputs = utils.cal.check_word(adjec, words)
                        #break
                    else: #appos
                        appos = utils.alg.simp_appos_sent(str(entries)) 
                        if len(appos) > 0:
                            outputs = utils.cal.check_word(appos, words) 
                            #break
                        else: #passive
                            passive = utils.alg.simp_passive_sent(str(entries)) 
                            if len(passive) > 0:
                                outputs = utils.cal.check_word(passive, words) 
                                #break
                            else: # just simplify the word
                                #outputs = utils.cal.check_word(entries, words)
                                pass
                  
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
