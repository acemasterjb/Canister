from flask import abort, Blueprint, g, flash
from flask import redirect, render_template, request

from blog.blog.blog_view import get_post
from blog.blog.model import Comment


bp = Blueprint('single_post', __name__)


def get_comment(id, check_author=True):
    comment = Comment.query.get(id)

    if comment is None:
        abort(404, "Comment id {} not found".format(id))

    if check_author and comment['author_id'] != g.user.uid:
        abort(403)
    return comment


@bp.route('/post/<int:id>', methods=('GET', 'POST'))
def post(id):

    from blog.auth.model import User

    post = get_post(id, False)

    comments = Comment.query.filter_by(parent_post=post).all()

    if request.method == 'POST':
        comment = request.form['comment']
        error = None

        if not comment:
            error = "Please add some content to your comment"

        if error is not None:
            flash(error)
        else:
            from blog import db
            comment = Comment(comment=comment,
                              author_id=g.user.uid, parent=post.id)
            db.session.add(comment)
            db.session.commit()

            return redirect('/post/{}'.format(id))

    return render_template('blog/post.html',
                           post=post, comments=comments, User=User)