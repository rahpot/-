import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Teacher(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'teachers'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    object = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=1)
    last_date = sqlalchemy.Column(sqlalchemy.DateTime)


