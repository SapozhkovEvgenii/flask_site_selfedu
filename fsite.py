from flask import (Flask, render_template, request, flash, g,
                   abort, session, redirect, url_for)
from config import SECRET_KEY, DB_PASSWORD, DB_USERNAME
import psycopg2
from format_db import FormatDataBase
from werkzeug.security import generate_password_hash, check_password_hash
import validators
import re
from user_login import UserLogin
from flask_login import (LoginManager, login_user, login_required,
                         logout_user, current_user)
from werkzeug.utils import secure_filename
import os
from forms import LoginForm, RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please log in"
login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().from_db(user_id, dbase)


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
@login_required
def show_post(alias):
    title, text = dbase.get_post(alias)
    if not title:
        abort(404)
    return render_template("show_post.html",
                           menu=dbase.get_menu(),
                           title=title, text=text)


@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.get_user_by_email(form.email.data)
        if user and check_password_hash(user['password'], form.password.data):
            userlogin = UserLogin().create(user)
            rm = form.remember.data
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("profile"))

        flash("Invalid email/password pair", category='error')

    return render_template("login.html", menu=dbase.get_menu(), title="Login",
                           form=form)


pattern_psw = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&-])[A-Za-z\d@$!%*#?&-]{8,}$'


@app.route("/register", methods=['POST', 'GET'])
def register():
    global pattern_psw
    form = RegisterForm()
    if form.validate_on_submit():
        session.pop('_flashes', None)
        if len(form.name.data) > 4 \
                and validators.email(form.email.data) \
                and re.match(pattern_psw, form.password.data) \
                and form.password.data == form.password_repeat.data:
            hash_psw = generate_password_hash(form.password.data)
            res = dbase.add_user(form.name.data,
                                 form.email.data,
                                 hash_psw)
            if res:
                flash('Registration successful', category='success')
                return redirect(url_for('login'))
            else:
                flash('[INFO] Error adding data in database', category='error')
        else:
            if len(form.name.data) < 4:
                flash("""Username has incorrect format.
                    You must use more than 4 characters""", category='error')
            if not validators.email(form.email.data):
                flash('Email has incorrect format.', category='error')
            if re.match(pattern_psw, form.password.data) is None:
                flash("""Password has incorrect format.
                    You have to use the following characters:
                    [a-z][A-Z][0-9][@$!%*#?&-]""", category='error')
            if form.password.data != form.password_repeat.data:
                flash('Passwords do not match.', category='error')

    return render_template(
        "register.html", menu=dbase.get_menu(),
        title="Registration", form=form)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html',
                           menu=dbase.get_menu(),
                           title='Profile')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out', category='success')
    return redirect(url_for('login'))


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.allowed_file_avatar(file.filename):
            try:
                filename = secure_filename(file.filename)
                file_path = os.path.join('static', 'images_html',
                                         'avatar', filename)
                file.save(file_path)
                try:
                    user_id = current_user.get_id()
                    res = dbase.upload_avatar(file_path, user_id)
                    if not res:
                        flash('Avatar upload successful', category='success')
                        return redirect(url_for('profile'))

                except Exception:
                    flash("[INFO] Error avatar upload", category='error')

            except FileNotFoundError:
                flash("File read error", category='error')

    return redirect(url_for('profile'))


if __name__ == "__main__":
    app.run(debug=True)
