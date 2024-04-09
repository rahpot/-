from flask import Flask
from flask import redirect
from flask import request
from flask import render_template
from flask import url_for
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_restful import Api

from data import db_session
from data.users import User
from data.teachers import Teacher
from data.dates import Date
from data.teach_sort import alph_sort, genre_sort, date_sort
from forms.add_teach import AddTeachForm
from forms.login import LoginForm
from forms.register import RegisterForm
from forms.teachers_form import TeachForm
from forms.teacher_page import TeacherPage
from forms.wallet import WalletForm

from datetime import datetime, timedelta

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'academlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

adm_password = '12435'


def main():
    db_session.global_init("db/teachers.db")

    @app.route('/', methods=['GET'])
    def top():
        params = {
            "title": 'Регистратор отработанных дней'}
        return render_template("top.html", **params)

    @app.route('/teachers_view',
               methods=['GET', 'POST'])  # Страница с учителями
    def teachers_view():
        form = TeachForm()
        db_sess = db_session.create_session()
        dates = db_sess.query(Date).all()
        dates.sort(key=lambda x: x.date_start)
        dates_interim = {}
        for date in dates:
            if date.teach_id in dates_interim.keys():
                continue
            dates_interim[date.teach_id] = date.date_start
        dates = dates_interim
        teachers = db_sess.query(Teacher).all()
        teachers = alph_sort(teachers)
        if form.sort_type.data == 'alph':
            teachers = alph_sort(teachers)
        elif form.sort_type.data == 'date':
            teachers = date_sort(teachers)
        elif not current_user.type:
            redirect('/')
        return render_template("teachers.html", teachers=teachers, dates=dates, form=form,
                               title='Учителя')

    @app.route('/teach_del/<int:id>',
               methods=['GET', 'POST'])  # Удаление учителя из своей библиотеки
    @login_required
    def teach_del(id):
        db_sess = db_session.create_session()
        teachers = db_sess.query(Teacher).filter(Teacher.id == id).first()
        if teachers:
            db_sess.delete(teachers)
            db_sess.commit()
        return redirect('/teachers_view')

    @app.route('/teacher/<int:id>', methods=['GET', 'POST'])  # Страница учителя
    def teach(id):
        form = TeacherPage()
        db_sess = db_session.create_session()
        teacher = db_sess.query(Teacher).filter(Teacher.id == int(id)).first()
        dates = db_sess.query(Date).filter(Date.teach_id == int(id)).all()
        if form.validate_on_submit():
            if not(form.date_start.data):
                return render_template('teacher_page.html', title=teacher.name,
                                       form=form, message="Не указана дата начала")
            if form.duration.data:
                form.date_end.data = form.date_start.data + timedelta(days=form.duration.data)
            date = Date(
                date_start=form.date_start.data,
                date_end=form.date_end.data,
                teach_id=teacher.id,
                type=form.get.data
            )
            if date.type == 1:
                c = int((date.date_end - date.date_start).days)
            if date.type == 0:
                c = int((date.date_start - date.date_end).days)
            teacher.count += c
            db_sess.add(date)
            db_sess.commit()
        return render_template("teacher_page.html", title=teacher.name, teacher=teacher,
                               dates=dates, form=form)

    @app.route('/add_teach', methods=['GET', 'POST'])  # Страница добавления учителя
    def add_teach():
        form = AddTeachForm()
        if form.validate_on_submit():
            if form.last_date.data > datetime.now().date():
                return render_template('add_teach.html', title='Добавление учителя',
                                       form=form, message="Неверный формат года")
            db_sess = db_session.create_session()
            teach = Teacher(
                name=form.name.data,
                object=form.sch_object.data,
                last_date=form.last_date.data
            )
            db_sess.add(teach)
            db_sess.commit()
            return redirect('/teachers_view')
        return render_template("add_teach.html", title='Добавление учителя', form=form)

    @app.route('/register', methods=['GET', 'POST'])  # Регистрация
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.r_password.data:
                return render_template('register.html', title='Регистрация',
                                       form=form, message="Пароли не совпадают")
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form, message="Логин занят")
            adm_type = False
            if form.type_password.data == adm_password:
                adm_type = True
            user = User(
                name=form.name.data,
                email=form.email.data,
                type=adm_type
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
        return render_template('register.html', title='Регистрация', form=form)

    @login_manager.user_loader
    def load_user(user_id):
        db_sess = db_session.create_session()
        return db_sess.query(User).get(user_id)

    @app.route('/login', methods=['GET', 'POST'])  # Вход
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for("teachers_view"))
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        return render_template('login.html', title='Авторизация', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    app.run()


if __name__ == '__main__':
    main()
