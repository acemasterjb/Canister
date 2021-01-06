import re

from flask import Blueprint, flash, g
from flask import redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from blog.auth.views import login_required
from blog.blog.model import Post
from blog.auth.model import User
from blog.pages.model import Page
from blog import db

bp = Blueprint('blog', __name__)
# pages = Page.query.all()


@bp.route('/')
def index():
    blog_name = ""  # change this to your blog's title
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.created_at.desc()).paginate(per_page=5, page=page)
    pages = Page.query.all()
    return render_template('blog/index.html', posts=posts,
                           pages=pages, User=User, blog_name=blog_name)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        pages = Page.query.all()
        title = request.form['title']
        body = request.form['body']
        error = None
        toc = False

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            print(body)
            try:
                if request.form['toc'] == 'yes':
                    toc = True
                    regex = re.compile(r'<h[1-6]>[a-zA-Z" "0-9]*</h[1-6]>')
                    headers = regex.findall(body)
                    # print(headers)
                    i = 1

                    for header in headers:
                        # start = body.find(header)
                        # end = body.find(header) + 1

                        h_link = r"<a id={0} href='#'>".format(i) \
                            + header + r"</a>"

                        body = re.sub(header, h_link, body)

                        i += 1
            except Exception:
                pass
            # for header in post, turn them into ancor links
            post = Post(title=title, body=body,
                        author_id=g.user.uid, toc=toc, pages=pages)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = Post.query.get(id)

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post.author_id != g.user.uid:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            db.session.commit()
            print(post.body)
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))
