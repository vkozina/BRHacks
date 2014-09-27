import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from flask.ext.sqlalchemy import SQLAlchemy
from database import init_db, db_session, Base
from models import User

# configuration
#DATABASE = 'C:/Temp/testing.db'
DEBUG = True
SECRET_KEY = 'development key'
USER = ''
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

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        newUsername = request.form['username']
        newPassword = request.form['password']
        user = User.query.filter_by(name=newUsername).first()
        if (user != None):
            error = 'Choose another username'
        else:
            newUser = User(newUsername, newPassword)
            db_session.add(newUser)
            db_session.commit()
            return redirect(url_for('login'))
    return render_template('signup.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        enteredUser = request.form['username']
        enteredPassword = request.form['password']
        u = User.query.filter_by(name=enteredUser).first()
        if (u == None):
            error = 'Invalid username'
        elif (enteredPassword != u.password):
            error = 'Invalid password'
        else:
            session['user'] = u.name
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_groups'))
    return render_template('login.html', error=error)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if not session.get('logged_in'):
        abort(401)
    u = User.query.filter_by(name=session.get('user')).first()
    u.profile = request.form['profile']
    #([request.form['profile'])
    db_session.commit()
    flash('Profile was edited')
    return redirect(url_for('show_groups'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/')
def show_groups():
    cur = g.db.execute('select title, text from groups order by id desc')
    groups = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_groups.html', groups=groups)

@app.route('/add_group', methods=['GET', 'POST'])
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