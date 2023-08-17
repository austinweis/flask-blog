from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
from werkzeug.security import check_password_hash, generate_password_hash

from awblog.db_manage import get_db
import functools

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_only(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('admin'):
            return view(**kwargs)

        return redirect(url_for('admin.login'))

    return wrapped_view

@bp.route('/', methods=('GET',))
@admin_only
def panel():
    # get posts from database
    db = get_db()
    curs = db.execute('SELECT * FROM posts ORDER BY created DESC')
    posts = curs.fetchall()
    db.close()
        
    return render_template('admin.html', title="Admin Panel", posts=posts)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'GET':
        return render_template('login.html', title="Admin Login")
    elif request.method == 'POST':
        if check_password_hash(current_app.config['ADMIN_PASSWORD'], request.form.get('password')):
            session['admin'] = True
            return redirect(url_for('admin.panel'))
        else:
            session['admin'] = False
            return redirect(url_for('blog.index'))