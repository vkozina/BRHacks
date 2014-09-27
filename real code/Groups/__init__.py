import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from flask.ext.sqlalchemy import SQLAlchemy
from database import init_db, db_session

# configuration
#DATABASE = 'C:/Temp/testing.db'
DEBUG = True
SECRET_KEY = 'development key'
#USERNAME = 'admin'
#PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
init_db()

def connect_db():
    #return sqlite3.connect(app.config['DATABASE'])
    return db_session

#def init_db():
#    with closing(connect_db()) as db:
#        with app.open_resource('schema.sql', mode='r') as f:
#            db.cursor().executescript(f.read())
#        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

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
    return redirect(url_for('login'))

@app.route('/')
def show_groups():
    cur = g.db.execute('select title, text from groups order by id desc')
    groups = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_groups.html', groups=groups)

@app.route('/add', methods=['POST'])
def add_group():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into groups (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New group was successfully posted')
    return redirect(url_for('show_groups'))

if __name__ == '__main__':
    app.run()