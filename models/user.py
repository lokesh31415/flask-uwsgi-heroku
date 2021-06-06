
import sqlite3
from config import DB_NAME
from db import db

class UserModel(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10))
    password = db.Column(db.String(15))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_by_username(cls, username):
       return cls.query.filter_by(username=username).first()

    @classmethod
    def fetch_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

