from flask import (Blueprint, request, redirect, url_for, flash,
                   render_template, session, g)
from psycopg2.extras import DictCursor

admin = Blueprint('admin', __name__, template_folder='templates',
                  static_folder='static')

menu = [{'url': '.index', 'title': 'Panel'},
        {'url': '.list_posts', 'title': 'List posts'},
        {'url': '.logout', 'title': 'Logout'}]

db = None


@admin.before_request
def before_request():
    global db
    db = g.get('link_db')


@admin.teardown_request
def teardown_request(request):
    global db
    db = None
    return request


def login_admin():
    session['admin_logged'] = 1


def is_logged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


@admin.route('/')
def index():
    if not is_logged():
        return redirect(url_for('.login'))

    return render_template('admin/index.html', menu=menu, title='Admin Panel')


@admin.route('/login', methods=["POST", "GET"])
def login():
    if is_logged():
        return redirect(url_for('.index'))
    if request.method == "POST":
        if request.form['user'] == "admin" and \
                request.form['password'] == "Tsz1985-es":
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash("Invalid user/password pair", category="error")

    return render_template('admin/login.html', title='Admin panel')


@admin.route('/logout', methods=["POST", "GET"])
def logout():
    if not is_logged():
        return redirect(url_for('.login'))

    logout_admin()

    return redirect(url_for('.login'))


@admin.route('/list_posts')
def list_posts():
    if not is_logged():
        return redirect(url_for('.login'))
    if db:
        try:
            cursor = db.cursor(cursor_factory=DictCursor)
            sql = "select title, url, text from posts order by date desc;"
            cursor.execute(sql)
            list = cursor.fetchall()
        except Exception as _ex:
            print("[INFO] Error reading from database", _ex)

    return render_template("admin/list_posts.html", menu=menu,
                           title="List posts", list=list)
