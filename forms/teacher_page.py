from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, BooleanField, IntegerField
from datetime import datetime


class TeacherPage(FlaskForm):
    date_start = DateField("Дата начала", default=(datetime.now()))
    date_end = DateField("Дата завершения", default=(datetime.now()))
    duration = IntegerField("Продолжительность")
    get = BooleanField("Полученные")
    submit = SubmitField("Добавить")
