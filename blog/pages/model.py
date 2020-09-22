from datetime import datetime

from blog.blog.model import User
from blog import db


class Page(db.Model):
    """
        Class for highest level web page.
    """
    path_name = db.Column(db.String(30), primary_key=True)
    page_name = db.Column(db.TEXT, nullable=False)
    author_id = db.Column(db.ForeignKey(User.uid), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    author = db.relationship(User, lazy="joined", backref="page")


class PageElement(db.Model):
    """
        Class for Page class elements.

        This class has a parent_page property that links this
        class with the Page class in the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.ForeignKey(User.uid), nullable=False)
    parent = db.Column(db.ForeignKey(Page.path_name), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.TEXT(16777216), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    parent_page = db.relationship(Page, lazy="joined", backref="page")
    author = db.relationship(User, lazy="joined", backref="pageElement")
