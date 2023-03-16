from datetime import datetime
from app import db


class Team(db.Model):
    __tablename__ = 'user_project_team'

    user_id =      db.Column(db.Integer(),   db.ForeignKey('users.id')),
    project_id =   db.Column(db.Integer(),   db.ForeignKey('projects.id')),
    role =         db.Column(db.String(70),  nullable=False)


class Sponsor(db.Model):
    __tablename__ = 'user_project_helper'

    user_id =      db.Column(db.Integer(),      db.ForeignKey('users.id')),
    project_id =   db.Column(db.Integer(),      db.ForeignKey('projects.id')),
    money =        db.Column(db.BigInteger(),   nullable=False)


class User(db.Model):
    __tablename__: str = 'users'

    id =                      db.Column(db.Integer(),       primary_key=True)
    name =                    db.Column(db.String(102),     nullable=False)
    nickname =                db.Column(db.String(30),      nullable=False)
    registered_on =           db.Column(db.DateTime(),      default=datetime.now)
    password =                db.Column(db.String(24),      nullable=False)
    email =                   db.Column(db.Text,            unique=True,         nullable=False)
    image_id =                db.Column(db.Integer(),       nullable=False)
    resume =                  db.Column(db.Text,            nullable=False)
    about_me =                db.Column(db.Text,            nullable=False)
    address =                 db.Column(db.Text,            nullable=False)
    projects_participated =   db.relationship('Project',    secondary=Team,      back_populates='users')
    projects_sponsored =      db.relationship('Project',    secondary=Sponsor,   back_populates='users')


class Project(db.Model):
    __tablename__: str = 'projects'

    id =                 db.Column(db.Integer(),    primary_key=True)
    author_id =          db.Column(db.Integer(),    db.ForeignKey('users.id'))
    users_clicked =      db.Column(db.Text,         nullable=True)
    caption =            db.Column(db.String(100),  nullable=False)
    image_id =           db.Column(db.Integer(),    nullable=False)
    created_on =         db.Column(db.DateTime(),   default=datetime.now)
    updated_on =         db.Column(db.DateTime(),   default=datetime.now,   onupdate=datetime.now)
    needed_amount =      db.Column(db.BigInteger(), nullable=False)
    received_amount =    db.Column(db.BigInteger(), nullable=False)
    description =        db.Column(db.Text,         nullable=False)
    address =            db.Column(db.Text,         nullable=False)
    team =               db.relationship('User',    secondary=Team,         back_populates='projects')
    sponsors =           db.relationship('User',    secondary=Sponsor,      back_populates='projects')
