from flask import (Blueprint, request, redirect, url_for, flash,
                   render_template, session)

admin = Blueprint('admin', __name__, template_folder='templates',
                  static_folder='static')

menu = [{'url': '.index', 'title': 'Panel'},
        {'url': '.logout', 'title': 'Logout'}]


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
