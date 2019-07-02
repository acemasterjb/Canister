from blog import db

# from blog.blog.post_view import Comment


class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    isAdmin = db.Column(db.Boolean, nullable=False)
    # comments = db.relationship(Comment, lazy="joined", backreff="users")

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.uid

    # Required for administrative interface
    def __unicode__(self):
        return self.username

    def __repr__(self):
        return "<User {}>".format(self.username)
