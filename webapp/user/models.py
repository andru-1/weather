from flask_login import UserMixin # стандартные определения залогинен пользваталь или нет, активен или нет...
from werkzeug.security import generate_password_hash, check_password_hash

from webapp.db import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)

    def set_password(self, password): # метод генерирует хеш от присланного пользователем пароля и рузельтат кладем в password
        self.password = generate_password_hash(password)

    def check_password(self, password): # метод сравнивает хеши в БД и присланное от пользвателя и возвратит тру или фолс
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return '<User name={} id={}>'.format(self.username, self.id)