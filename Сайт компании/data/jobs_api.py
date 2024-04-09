import flask
from flask import jsonify
from flask import request

from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=(
                    'id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date',
                    'end_date',
                    'is_finished'))
                    for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=["GET"])
def get_one_job(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({"error": 'Not found'})
    return jsonify(
        {
            "jobs": jobs.to_dict(
                only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date',
                      'end_date',
                      'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date',
                  'end_date',
                  'is_finished']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if db_sess.query(Jobs).filter(Jobs.id == request.json['id']):
        return jsonify({'error': 'Id already exists'})
    jobs = Jobs(
        id=request.json['id'],
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        start_date=request.json['start_date'],
        end_date=request.json['end_date'],
        is_finished=request.json['is_finished']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_news(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['POST'])
def red_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    print('ok')
    if not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators', 'start_date',
                  'end_date',
                  'is_finished']):
        return jsonify({'error': 'Bad request'})
    elif not jobs:
        return jsonify({'error': 'Not found'})
    jobs.team_leader = request.json['team_leader'],
    jobs.job = request.json['job'],
    jobs.work_size = request.json['work_size'],
    jobs.collaborators = request.json['collaborators'],
    jobs.start_date = request.json['start_date'],
    jobs.end_date = request.json['end_date'],
    jobs.is_finished = request.json['is_finished']
    db_sess.commit()
    return jsonify({'success': 'OK'})