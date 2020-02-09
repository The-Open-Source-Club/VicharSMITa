from app import db
from datetime import datetime
from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Integer)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User <<{}>> {}>'.format(self.role, self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator = db.Column(db.Integer, index=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(512), index=True, unique=True)
    brief = db.Column(db.UnicodeText(), index=True)
    content = db.Column(db.UnicodeText(), index=True)
    tags = db.Column(db.UnicodeText(), index=True)
    likes = db.Column(db.Integer, default = 0)
    imageurl = db.Column(db.UnicodeText(), index=True)
    likedusers = db.Column(db.UnicodeText(), index=True)
    def __repr__(self):
        return '<Article {} :: {}>'.format(self.id, self.title)
