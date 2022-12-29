from app import db, login_manager
from flask_login import LoginManager, UserMixin
from sqlalchemy import UniqueConstraint
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from hashlib import md5
class Users(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), nullable=False, unique=True)
    nickname = db.Column(db.String(30), nullable=False, unique=True)
    profile_image = db.Column(db.String(100))
    email = db.Column(db.String(100))
    date_of_create = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    password_hash = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Users %r>' % self.id

    def __init__(self, *args, **kwargs):
        super(Users, self).__init__(*args, **kwargs)

    def generate_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return  check_password_hash(self.password_hash, password)

    def avatar(self):
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(64)


@login_manager.user_loader
def load_user(user):
    return Users.get(user)

class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    title_category = db.Column(db.String(100), nullable=False)
    description_category = db.Column(db.Text)
    creator_of_category = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        super(Categories, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Categories %r>' % self.id

class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title_post = db.Column(db.String(100), nullable=False)
    short_description_of_post = db.Column(db.String(150))
    post_image = db.Column(db.Text)
    post_body = db.Column(db.Text)
    post_creator = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    date_create = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    last_redactor = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    date_of_last_redact = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    post_category = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        super(Posts, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Posts %r>' % self.id

class Comments(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    date_post = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    author = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    comment_body = db.Column(db.Text)
    comment_post = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        super(Comments, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Comments %r>' % self.id

