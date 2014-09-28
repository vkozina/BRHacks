import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from flask.ext.sqlalchemy import SQLAlchemy
from database import init_db, db_session, Base
from models import User, Groups
from rhinetest import Rhine
import math

# configuration
#DATABASE = 'C:/Temp/testing.db'
DEBUG = True
SECRET_KEY = 'development key'
USER = ''
s = Rhine('sdf0b913e4b07b5243b7f527')
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

@app.route('/')
def home():
    return render_template('home.html')

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
    error = None
    u = User.query.filter_by(name=session.get('user')).first()
    if request.method == 'POST':
        u.profile = request.form.get('profile')
        #([request.form['profile'])
        db_session.commit()
        flash('Profile was edited')
        return redirect(url_for('show_groups'))
    return render_template('edit_profile', enteredText=u.profile)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    flash('You were logged out')
    return redirect(url_for('home'))

@app.route('/show')
def show_groups():
    if not session.get('logged_in'):
        return redirect(url_for('home'))
    
    groups = Groups.query.order_by(Groups.id)
    user = User.query.filter_by(name=session.get('user')).first()

    if (user.profile != None):
        userText = user.profile.split()
        groupList = list()
        order = list()
        for group in groups:
            groupText = group.text.split()
            difference = compareTexts(userText, groupText)
            groupList.append(group)
            if math.isnan(difference):
                difference = 1000
            order.append(difference)

        #session['groupOrder'] = order
        if len(order) > 0:
            groups = sort(order, groupList)
    return render_template('show_groups.html', groups=groups)

def compareTexts(text1, text2):
    '''
    totalDistance = 0
    for word1 in text1:
        for word2 in text2:
            totalDistance += s.distance(word1, word2)
    return totalDistance
    '''
    return s.distance(text1, text2)

def sort(order, groups):
    order, groups = zip(*sorted(zip(order, groups)))
    order, groups = (list(t) for t in zip(*sorted(zip(order, groups))))
    return groups

@app.route('/add_group', methods=['GET', 'POST'])
def add_group():
    if not session.get('logged_in'):
        abort(401)
    error = None
    if request.method == 'POST':
        newGroup = Groups(request.form['title'], request.form['text'], request.form['contact'])
        db_session.add(newGroup)
        db_session.commit()
        #g.db.execute('insert into groups (title, text) values (?, ?)',
        #         [request.form['title'], request.form['text']])
        #g.db.commit()
        flash('New group was successfully posted')
        return redirect(url_for('show_groups'))
    return render_template('add_group', error=error)
    
@app.route('/single_profile')
def single_profile():
    name = request.args.get('name')
    des = Groups.query.filter_by(title=name).first()
    desc=des.text
    contact = des.contact
    return render_template('single_profile', data = name, descript=desc, contact=contact, method = 'single_profile')

if __name__ == '__main__':
    app.run()
