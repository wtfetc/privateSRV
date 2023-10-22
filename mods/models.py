from flask_login import UserMixin

from mods import db


class UserAuth(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    group = db.Column(db.String(255), nullable=False)
    b24_id = db.Column(db.Integer)
