from flask_wtf import FlaskForm
from wtforms import SubmitField


class BookPageForm(FlaskForm):
    buy = SubmitField('Приобрести')
