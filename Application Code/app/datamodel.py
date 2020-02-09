from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Integer)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    

    def __repr__(self):
        return '<User <<{}>> {}>'.format(selfself.username)    


class Article(db.Model)
	id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512), index=True, unique=True)
    content = db.Column(db.UnicodeText(), index=True)

    def __repr__(self):
        return '<Article {} :: {}>'.format(self.id, self.title);  
