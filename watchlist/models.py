from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from watchlist import db


class User(db.Model, UserMixin):  # 用户表
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(255))
    nickname = db.Column(db.String(20))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)
