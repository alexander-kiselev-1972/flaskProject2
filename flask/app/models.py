from . import db


class User(db.Model):
    __tablename__='user_own'
    id = db.Column(db.INTEGER, primary_key=True)

class Role(db.Model):
    __tablename__='role'
    id = db.Column(db.INTEGER, primary_key=True)