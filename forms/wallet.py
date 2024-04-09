from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, IntegerField


class WalletForm(FlaskForm):
    money = IntegerField('Сумма')
    card = IntegerField('Номер карты')
    password = PasswordField('Пароль пришедший на телефон')
    ok = SubmitField('Подтвердить')
