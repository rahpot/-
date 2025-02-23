from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField, BooleanField


class LibForm(FlaskForm):
    sort_type = SelectField("Тип сортировки",
                            choices=[('alph', 'по алфавиту'), ('date', 'по дате')])
    genre_type = SelectField("Жанр",
                             choices=[(1, 'Любой'), (2, 'Деловая литература'),
                                      (3, 'Детективы и Триллеры'),
                                      (4, 'Документальная литература'),
                                      (5, 'Дом, ремесла, досуг, хобби'), (6, 'Драматургия'),
                                      (7, 'Искусство, Искусствоведение, Дизайн'),
                                      (8, 'Компьютеры и Интернет'), (9, 'Литература для детей'),
                                      (10, 'Любовные романы'), (11, 'Наука, Образование'),
                                      (12, 'Поэзия'), (13, 'Приключения'), (14, 'Проза'),
                                      (15, 'Прочее'),
                                      (16, 'Религия, духовность, эзотерика'),
                                      (17, 'Справочная литература'), (18, 'Старинное'),
                                      (19, 'Техника'),
                                      (20, 'Учебники и пособия'), (21, 'Фантастика'),
                                      (22, 'Фольклор'),
                                      (23, 'Юмор'), (24, 'Здоровье, красота, психология'),
                                      (25, 'Зарубежная литература')])
    name = StringField("Название книги", default="Название книги")
    author = StringField("Имя автора", default="Имя автора")
    only_my = BooleanField("Только мои работы")
    submit = SubmitField("Поиск")
