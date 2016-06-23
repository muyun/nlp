# -*- coding: utf-8 -*-
# coding by wenlong 
#
import os
import sqlite3
#from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort,\
    render_template, flash

# the dataset
import utils.dt as dt

# the application
app = Flask(__name__)
app.config.from_object(__name__)

# load default config
app.config.update(dict(
    # the Database Path
    DATABASE=os.path.join(app.root_path,'simptext.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='admin'
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


# database
def connect_db():
    """ database connection"""
    rv = sqlite3.connect(app.config['DATABASE'])
    # row
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """initializes the database"""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """create the database tables"""
    init_db()
    print 'Initialized the database'

def get_db():
    """ opens a new database connection """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

"""
functions marked with teardown_appcontext() are called
"""
@app.teardown_appcontext
def close_db(error):
    """close the database again at the end of the request"""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


#the view functions - the view shows all the entries stored in the database
@app.route('/')
def show_entries():
    db = get_db()
    #cur = db.execute('select input from entries order by id desc')
    #entries = cur.fetchall()

    #cur = db.execute('select output from rets where id=(select max(id) from rets)')
    #entries = cur.fetchall()
    #print "output: ", entries

    cur = db.execute('select entries.input, rets.output from entries, rets  where rets.id=entries.id and rets.id=(select max(rets.id) from rets)')
    entries = cur.fetchall()
    print "output: ", entries
             
    return render_template('show_entries.html', entries=entries)

# get the result
# TODO:
@app.route('/output')
def get_outputs():
    db = get_db()
    cur = db.execute('select entries.input, rets.output from entries, rets  where rets.id=(select max(rets.id) from rets)')
    rets = cur.fetchall()
    print "rets-: ", rets
    
    #print "rets: ", rets 
    return render_template('show_entries.html', rets=rets)

# this view let the user add new entries if they are logged in
@app.route('/add', methods=['POST'])  # URL with a variable
def add_entry():                      # The function shall take the URL variable as parameter
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries(input) values (?)',
               [request.form['input']])

    #cur = db.execute('select id from entries right join entries on rets.id=entries.id')
    
    # the simplied words
    filename = '/Users/zhaowenlong/workspace/proj/dev.nlp/web/simptext/utils/wordlist.xlsx'
    words = dt.read_file(filename)
    # simplify the words in entries.input
    ret = dt.check_word(request.form['input'], words)
    print "ret: ", ret
       
    db.execute('insert into rets(output) values (?)',
               [ret]) 

    db.commit()
    flash('New entry was successfully posted')

    entries=[request.form['input'], ret]
    print "entries: ", entries
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
