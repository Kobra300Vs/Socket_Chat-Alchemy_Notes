from .db_app import db
from flask_login import UserMixin
from sqlalchemy.sql import func
# All Data Base schemes


# ID of note; Data = content of Note; Date of Note; ID_user -> reference to User.ID who save Note
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))


# ID of User; email of User; Nickname of User; pwd -> password of User
# Notes and Posts references to each User
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    nick = db.Column(db.String(70))
    pwd = db.Column(db.String(64))
    notes = db.relationship('Note')
    posts = db.relationship('Message')


# ID of chat Message; data -> content of Message; date of Message; id_user -> which User public this
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(500))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))

# Maybe in future?
# class Mod(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
#
# class BannedEMail(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.Integer, db.ForeignKey('user.email'))
