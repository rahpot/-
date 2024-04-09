import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Date(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'dates'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    date_start = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    date_end = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    teach_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    type = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)