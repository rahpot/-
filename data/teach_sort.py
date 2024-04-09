from . import db_session
from .genres import Genre
from datetime import datetime


def alph_sort(books):
    books = sorted(books, key=lambda book: book.name)
    return books


def date_sort(books):
    books = sorted(books, key=lambda book: book.last_date)
    return books

def genre_sort(books, genre):
    db_sess = db_session.create_session()
    genre_id = db_sess.query(Genre).filter(Genre.id == genre).first()
    books = list(filter(lambda book: book.genre == genre_id.id, books))
    return books
