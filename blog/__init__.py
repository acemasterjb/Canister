import os
import click
from flask import Flask, url_for

from flask_sqlalchemy import SQLAlchemy  # https://git.io/fjSr8
from flask.cli import with_appcontext

from flask_admin import Admin  # http://tiny.cc/exbhaz
from blog.admin.models import MyModelView
# from flask_admin.menu import MenuLink

from flask_login import LoginManager  # https://git.io/fjSrc

# markdown renderer
import markdown
from flask import Markup
# from jinja2 import Environment, PackageLoader, select_autoescape
# from flask_misaka import Misaka  # http://tiny.cc/7ybhaz

# from blog.blog import User, Post

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    db_url = os.environ.get("DATABASE_URL")
    if db_url is None:
        # This should be changed for your own configuration
        db_url = "mysql+mysqlconnector://root:djdI7f8tu@localhost/flask"

    # Change this secret key PLEASE http://tiny.cc/q3bhaz
    app.config.from_mapping(SECRET_KEY='VfuhtDAxKTKsFSWppGccfA==',
                            SQLALCHEMY_DATABASE_URI=db_url,
                            FLASK_ADMIN_SWATCH='superhero',
                            )

    admin = Admin(app, name='blog', template_mode='bootstrap3')

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    """This section sets up Flask Login; see Flask Login docs for more info"""
    init_login(app)

    from blog.blog.model import Post, Comment
    from blog.auth.model import User
    from blog.pages.model import Page, PageElement
    from . import db

    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Comment, db.session))
    admin.add_view(MyModelView(Post, db.session))
    admin.add_view(MyModelView(Page, db.session))
    admin.add_view(MyModelView(PageElement, db.session))

    # admin.add_link(MenuLink(name='Public Website', category='', url=url_for('blog.index')))
    """END SECTION"""

    db.init_app(app)
    app.cli.add_command(init_db_command)

    from blog.auth import views
    app.register_blueprint(views.bp)

    from blog.blog import blog_view, post_view
    app.register_blueprint(blog_view.bp)
    app.register_blueprint(post_view.bp)

    from blog.pages import page_view
    app.register_blueprint(page_view.bp)

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

    @app.template_filter('markdown')
    def md(text):
        return(Markup(markdown.markdown(text)))

    app.jinja_env.filters['markdown'] = md

    return app


def init_db():
    db.drop_all()
    db.create_all()


def init_login(app, login_manager=login_manager):
    """Initializes the login section of the web app. See
       Flask Login docs for more"""
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
