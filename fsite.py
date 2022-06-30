from flask import (Flask, render_template, request, flash, g,
                   abort, session, redirect, url_for)
from config import SECRET_KEY, DB_PASSWORD, DB_USERNAME
import psycopg2
from format_db import FormatDataBase
from werkzeug.security import generate_password_hash
import validators
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


def connect_db():
    connection = psycopg2.connect(
        host='localhost',
        database='flask_selfedu',
        user=DB_USERNAME,
        password=DB_PASSWORD
    )

    return connection


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None


@app.before_request
def before_request():
    """Get database connection before executing query"""
    global dbase
    db = get_db()
    dbase = FormatDataBase(db)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/")
def index():
    return render_template('index.html',
                           menu=dbase.get_menu(),
                           posts=dbase.get_all_posts())


@app.route("/add_post", methods=['POST', 'GET'])
def add_post():
    if request.method == 'POST':
        if len(request.form['title']) > 3 and len(request.form['text']) > 10:
            result = dbase.add_post(
                request.form['title'],
                request.form['url'],
                request.form['text'])
            if not result:
                flash('Error addiing post', category='error')
            else:
                flash('Article added successfully', category='success')
        else:
            flash('Error addiing post', category='error')

    return render_template('add_post.html',
                           menu=dbase.get_menu(),
                           title='Adding post')


@app.route("/posts/<alias>")
def show_post(alias):
    title, text = dbase.get_post(alias)
    if not title:
        abort(404)
    return render_template("show_post.html",
                           menu=dbase.get_menu(),
                           title=title, text=text)


@app.route("/login")
def login():
    return render_template("login.html", menu=dbase.get_menu(), title="Login")


pattern_psw = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&-])[A-Za-z\d@$!%*#?&-]{8,}$'


@app.route("/register", methods=['POST', 'GET'])
def register():
    global pattern_psw
    if request.method == 'POST':
        session.pop('_flashes', None)
        if len(request.form['name']) > 4 \
                and validators.email(request.form['email']) \
                and re.match(pattern_psw, request.form['psw']) \
                and request.form['psw'] == request.form['psw2']:
            hash_psw = generate_password_hash(request.form['psw'])
            res = dbase.add_user(request.form['name'],
                                 request.form['email'],
                                 hash_psw)
            if res:
                flash('Registration successful', category='success')
                return redirect(url_for('login'))
            else:
                flash('[INFO] Error adding data in database', category='error')
        else:
            if len(request.form['name']) < 4:
                flash("""Username has incorrect format.
                    You must use more than 4 characters""", category='error')
            if re.match(pattern_psw, request.form['psw']) is None:
                flash("""Password has incorrect format.
                    You have to use the following characters:
                    [a-z][A-Z][0-9][@$!%*#?&-]""", category='error')
            if not validators.email(request.form['email']):
                flash('Email has incorrect format.', category='error')
            if request.form['psw'] != request.form['psw2']:
                flash('Passwords do not match.', category='error')

    return render_template(
        "register.html",
        menu=dbase.get_menu(),
        title="Registration")


if __name__ == "__main__":
    app.run(debug=True)
