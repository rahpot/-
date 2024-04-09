from flask_restful import abort, Resource
from flask import jsonify
from sqlal.app.data import db_session
from sqlal.app.data.jobs import Jobs
from sqlal.app.resours.argumets_for_JobsListResource import parser


def abort_if_jobs_not_found(jobs_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        abort(404, message=f"User {jobs_id} not found")


class JobsResource(Resource):
    def get(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        return jsonify({'jobs': jobs.to_dict(only=('id', 'team_leader', 'job', 'work_size',
                                                   'collaborators', 'start_date',
                                                   'end_date',
                                                   'is_finished'))})

    def delete(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        session.delete(jobs)
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify(
            {'jobs': [item.to_dict(only=('id', 'team_leader', 'job', 'work_size',
                                         'collaborators', 'start_date',
                                         'end_date',
                                         'is_finished')) for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        jobs = Jobs(
            surname=args('surname'),
            name=args('name'),
            age=args('age'),
            position=args('position'),
            speciality=args('speciality'),
            address=args('address'),
            email=args('email')
        )
        session.add(jobs)
        session.commit()
        return jsonify({'success': 'OK'})
