import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    type = sqlalchemy.Column(sqlalchemy.Integer)


    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)