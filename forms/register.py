from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Логин/почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    r_password = PasswordField('Повторите пороль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    type_password = PasswordField('Пароль администратора')
    submit = SubmitField('Зарегистрироваться')

