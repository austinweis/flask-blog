from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, escape, current_app, get_flashed_messages
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from awblog.admin import admin_only
from awblog.db_manage import get_db
from markdown import markdown

import os

bp = Blueprint('blog', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/')
def index():
    # get ten newest posts from database
    db = get_db()
    curs = db.execute('SELECT * FROM posts ORDER BY created DESC LIMIT 10')
    posts = curs.fetchall()

    return render_template('index.html', title="Austin's Site", posts=posts)

@bp.route('/post/<int:post_id>')
def view_post(post_id):
    db = get_db()
    curs = db.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
    post = curs.fetchone()

    if post == None:
        abort(404)

    return render_template('post.html', title=post['title'], body=post['body'])

@bp.route('/posts')
def all_posts():
    posts = get_db().execute('SELECT * FROM posts ORDER BY id DESC').fetchall()

    return render_template('posts.html', title='All Posts', posts=posts)

@bp.route('/upload_image', methods=('POST',))
@admin_only
def upload_image():
    image = request.files.get('image')
    error = False

    if not image or image.filename == '': 
        flash('No file selected', 'file')
        error = True
    filename = secure_filename(image.filename)
    if not allowed_file(filename) and filename != '':
        flash('File type not supported', 'file')
        error = True
    if not error:
        image.save(os.path.join(current_app.config['UPLOADS_FOLDER'], filename))
        flash('File uploaded', 'success')
        
    return redirect(url_for('admin.panel'))


@bp.route('/create_post', methods=('POST',))
@admin_only
def create_post():
    title = request.form.get('title')
    file = request.files.get('file')
    error = False

    if not title or title == '':
        flash('No title given', 'post')
        error = True
    if not file or file.filename == '':
        flash('No file selected', 'post')
        error = True
    if not error:
        body = file.read().decode()
        db = get_db()
        db.execute('INSERT INTO posts (title, body) VALUES (?, ?)', (title, markdown(body)))
        db.commit()
        flash('Post uploaded', 'success')

    return redirect(url_for('admin.panel'))

@bp.route('/delete_post', methods=('POST',))
@admin_only
def delete_post():
    post_id = request.form.get('id')

    if post_id:
        db = get_db()
        db.execute('DELETE FROM posts WHERE id = ?', (post_id,))
        db.commit()
        flash('Post deleted', 'success')
    else:
        flash('No post selected', 'delete')
    return redirect(url_for('admin.panel'))