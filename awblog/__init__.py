import os

from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, send_from_directory, render_template, escape

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        APP_NAME='My Blog',
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'blog.sqlite'),
        ADMIN_PASSWORD=generate_password_hash('dev'),
        UPLOADS_FOLDER=os.path.join(app.instance_path, 'uploads/'),
        ALLOWED_EXTENSIONS = ('webm', 'svg', 'png', 'jpg', 'jpeg', 'gif', 'md')
    )
    app.root_path
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initialize db
    from . import db_manage
    with app.app_context():
        db_manage.init_db()

    # root static overrides
    @app.route('/robots.txt')
    @app.route('/sitemap.xml')
    def static_from_root():
        return send_from_directory(app.static_folder, request.path[1:])
    
    # serve from upload folder
    @app.route('/uploads/<string:upload>')
    def serve_upload(upload):
        return send_from_directory(app.config['UPLOADS_FOLDER'], escape(upload))

    # error templates
    @app.errorhandler(404)
    def page_not_found(e):
        # note that we set the 404 status explicitly
        return render_template('404.html'), 404

    # register blueprints
    from . import admin, blog, misc
    app.register_blueprint(admin.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(misc.bp)

    return app
