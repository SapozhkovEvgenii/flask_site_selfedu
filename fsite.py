from flask import Flask, render_template, request, flash, g, abort
from config import SECRET_KEY, DB_PASSWORD, DB_USERNAME
import psycopg2
from format_db import FormatDataBase


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


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/")
def index():
    db = get_db()
    dbase = FormatDataBase(db)
    return render_template('index.html',
                           menu=dbase.get_menu(),
                           posts=dbase.get_all_posts())


@app.route("/add_post", methods=['POST', 'GET'])
def add_post():
    db = get_db()
    dbase = FormatDataBase(db)
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
    db = get_db()
    dbase = FormatDataBase(db)
    title, text = dbase.get_post(alias)
    if not title:
        abort(404)
    return render_template("show_post.html",
                           menu=dbase.get_menu(),
                           title=title, text=text)


if __name__ == "__main__":
    app.run(debug=True)
