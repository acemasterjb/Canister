import os
import click
from flask import Flask, url_for

from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext

from flask_admin import Admin
from blog.admin.models import MyModelView

from flask_login import LoginManager

# from blog.blog import User, Post

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    admin = Admin(app, name='blog', template_mode='bootstrap3')
    db_url = os.environ.get("DATABASE_URL")

    if db_url is None:
        db_url = "sqlite:///" + os.path.join(app.instance_path, "blog")

    app.config.from_mapping(SECRET_KEY='VfuhtDAxKTKsFSWppGccfA==',
                            SQLALCHEMY_DATABASE_URI=db_url,
                            FLASK_ADMIN_SWATCH='superhero',
                            )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    init_login(app)

    from blog.blog.model import Post
    from blog.blog.model import Comment
    from blog.auth.model import User
    from . import db

    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Comment, db.session))
    admin.add_view(MyModelView(Post, db.session))

    db.init_app(app)
    app.cli.add_command(init_db_command)

    from blog.auth import views
    app.register_blueprint(views.bp)

    from blog.blog import blog_view
    app.register_blueprint(blog_view.bp)

    from blog.blog import post_view
    app.register_blueprint(post_view.bp)

    @app.context_processor
    def override_url_for():
        return dict(url_for=dated_url_for)

    def dated_url_for(endpoint, **values):
        if endpoint == 'static':
            filename = values.get('filename', None)
            if filename:
                file_path = os.path.join(app.root_path,
                                         endpoint, filename)
                values['q'] = int(os.stat(file_path).st_mtime)
        return url_for(endpoint, **values)

    return app


def init_db():
    db.drop_all()
    db.create_all()


def init_login(app, login_manager=login_manager):
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        from blog.auth.model import User
        return User.query.get(user_id)


# click.command() defines a command line command
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


# def init_app(app):
#     # app.teardown_appcontext() tells Flask to call that function
#     # when cleaning up after returning the response.
#     app.teardown_appcontext(close_db)

#     # app.cli.add_command() adds a new command that
#     # can be called with the flask command.
#     app.cli.add_command(init_db_command)
