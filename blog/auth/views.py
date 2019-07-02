import functools

from flask import (
    Blueprint, flash, g, redirect,
    render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from blog.auth.model import User

# create a bluepriny
# a Blueprint is a group of views and code that will be run when
# certain actions are called
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():

    from blog import db

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif User.query.filter_by(username=username) is None:
            error = 'User {} is already registered.'.format(username)

            # fetchone() returns one row from the query

        if error is None:
            user = User(username=username,
                        password=generate_password_hash(password),
                        email=email,
                        isAdmin=1)
            db.session.add(user)

            # generate_password_hash() is used to securely hash the password

            # Save the changes
            # After storing the user, they are redirected to the login page
            db.session.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        # check_password_hash
        # hashes the submitted password in the same way as
        # the stored hash and securely compares them

        if error is None:
            session.clear()
            session['user_id'] = user.uid
            return redirect(url_for('blog.index'))

        flash(error)

    return render_template('auth/login.html')


# bp.before_app_request() registers a function that runs
# before the view function, no matter what URL is requested
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
