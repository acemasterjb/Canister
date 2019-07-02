from flask import redirect, request, url_for
import flask_admin as admin
from flask_admin.contrib import sqla
import flask_login as login


class MyModelView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated and login.current_user.isAdmin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('admin.index', next=request.url))


class MyAdminIndexView(admin.AdminIndexView):
    @admin.expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.loginview'))
        return super(MyAdminIndexView, self).index()

    @admin.expose('/login/', methods=('GET', 'POST'))
    def loginview(self):
        from blog.auth.model import User
        from flask import check_password_hash, session
        from flask import flash, render_template

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
            return redirect(render_template('admin/index.html'))

        flash(error)

        return super(MyAdminIndexView, self).index()
