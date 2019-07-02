from datetime import datetime

from blog.auth.model import User
from blog import db


class Post(db.Model):
    """docstring for Post"""

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.ForeignKey(User.uid), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    author = db.relationship(User, lazy="joined", backref="posts")


class Comment(db.Model):
    """"""

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.ForeignKey(User.uid), nullable=False)
    parent = db.Column(db.ForeignKey(Post.id), nullable=False)
    comment = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    post_author = db.relationship(User, lazy="joined", backref="comments")
    parent_post = db.relationship(Post, lazy="joined", backref="comments")

    def __repr__(self):
        return "<Comment {0}> <User {1}>".format(self.id, self.author_id)
