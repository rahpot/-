from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField


class TeachForm(FlaskForm):
    sort_type = SelectField("Тип сортировки",
                            choices=[('alph', 'по алфавиту'), ('date', 'по дате')])
    sch_object = StringField("Школьный предмет")
    name = StringField("ФИО", default="ФИО")
    submit = SubmitField("Поиск")
