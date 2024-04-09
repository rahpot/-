from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField, DateField
from wtforms.validators import DataRequired
from datetime import datetime


class AddTeachForm(FlaskForm):
    name = StringField("ФИО", default="ФИО")
    sch_object = StringField("Школьный предмет")
    last_date = DateField('Дата изменения', default=datetime.now(), validators=[DataRequired()])
    submit = SubmitField("Добавить")
