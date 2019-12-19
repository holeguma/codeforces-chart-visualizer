from flask_sqlalchemy import SQLAlchemy

from main import db

user_problem_tbl = db.Table('users_problems', db.metadata, db.Column('user_id', db.Integer, db.ForeignKey(
    'users.id')), db.Column('problem_id', db.Integer, db.ForeignKey('problems.id')))
problem_tag_tbl = db.Table('problems_tags', db.metadata, db.Column('problem_id', db.Integer, db.ForeignKey(
    'problems.id')), db.Column('tag_id', db.Integer, db.ForeignKey('problem_tag.id')))


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String)
    country = db.Column(db.String)
    rating = db.Column(db.Integer)
    difficulty_sum = db.Column(db.Integer)
    cur_streak = db.Column(db.Integer)
    max_streak = db.Column(db.Integer)
    updated_at = db.Column(db.Date)
    tags = db.relationship('user_tag', backref='users')
    contests = db.relationship('Contest', backref='users')
    problems = db.relationship('Problem', secondary=user_problem_tbl)


class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String)
    tags = db.relationship('country_tag', backref='countries')


class Contest(db.Model):
    __tablename__ = 'contests'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    newRating = db.Column(db.Integer)
    oldRating = db.Column(db.Integer)
    rank = db.Column(db.Integer)
    contestID = db.Column(db.Integer)

class finished_contest(db.Model):
    __tablename__='finished_contest'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    contestID = db.Column(db.Integer)

class user_tag(db.Model):
    __tablename__ = 'user_tag'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    rating = db.Column(db.Integer)
    solved = db.Column(db.Integer)


class country_tag(db.Model):
    __tablename__ = 'country_tag'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    rating = db.Column(db.Integer)
    solved = db.Column(db.Integer)


class Problem(db.Model):
    __tablename__ = 'problems'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String)
    contestID = db.Column(db.Integer)
    index = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    solvedCount = db.Column(db.Integer)
    tags = db.relationship("problem_tag", secondary=problem_tag_tbl)


class problem_tag(db.Model):
    __tablename__ = 'problem_tag'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String)


def init():
    db.create_all()
