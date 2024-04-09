from flask import Flask
from flask import url_for
from sqlal.app.data import db_session
from sqlal.app.data.users import User
from sqlal.app.data.jobs import Jobs
from sqlal.app.data.departments import Departments
from flask import render_template
from flask import redirect
from flask_login import LoginManager
from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user
from sqlal.app.forms.register import RegisterForm
from sqlal.app.forms.login import LoginForm
from sqlal.app.forms.add_job import AddJobForm
from sqlal.app.data import db_session, jobs_api
from sqlal.app.resours import users_resource
from sqlal.app.resours import jobs_resource
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/blogs.db")

    db_session.global_init("db/blogs.db")
    app.register_blueprint(jobs_api.blueprint)

    @app.route('/')
    def top():
        params = {
            "title": 'главная'}
        return render_template("top.html", **params)

    @app.route('/jobs')
    def run_jobs():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter()
        return render_template("jobs.html", title="Работы", jobs=jobs)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.r_password.data:
                return render_template('register.html', title='Регистрация',
                                       form=form, message="Пароли не совпадают")
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == form.login.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form, message="Логин занят")
            user = User(
                surname=form.surname.data,
                name=form.name.data,
                position=form.position.data,
                age=form.age.data,
                address=form.address.data,
                speciality=form.speciality.data,
                email=form.login.data
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

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for("run_jobs"))
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        return render_template('login.html', title='Авторизация', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    @app.route('/add_jobs', methods=["GET", "POST"])
    def add_jobs():
        form = AddJobForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            if not db_sess.query(Jobs).filter(Jobs.team_leader == form.team_leader.data).first():
                return render_template('add_jobs.html', title='Добавление Работы',
                                       form=form, message="Такого капитана команды нет")
            job = Jobs(
                job=form.job.data,
                team_leader=form.team_leader.data,
                work_size=form.work_size.data,
                collaborators=form.collaborators.data,
                is_finished=form.is_finished.data,
            )
            db_sess.add(job)
            db_sess.commit()
            return redirect(url_for("run_jobs"))
        return render_template('add_jobs.html', title='Добавление работы', form=form)

    api.add_resource(users_resource.UsersListResource, '/api/v2/users')

    api.add_resource(users_resource.UserResource, '/api/v2/users/<int:user_id>')

    api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')

    api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:jobs_id>')

    app.run()


if __name__ == '__main__':
    main()
