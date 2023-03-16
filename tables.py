from datetime import datetime
from app import db


class Team(db.Model):
    __tablename__ = 'user_project_team'

    userId =      db.Column(db.Integer(),   db.ForeignKey('users.id')),
    projectId =   db.Column(db.Integer(),   db.ForeignKey('projects.id')),
    role =         db.Column(db.String(70),  nullable=False)


class Sponsor(db.Model):
    __tablename__ = 'user_project_helper'

    userId =      db.Column(db.Integer(),      db.ForeignKey('users.id')),
    projectId =   db.Column(db.Integer(),      db.ForeignKey('projects.id')),
    money =        db.Column(db.BigInteger(),   nullable=False)


class User(db.Model):
    __tablename__: str = 'users'

    id =                      db.Column(db.Integer(),       primary_key=True)
    name =                    db.Column(db.String(102),     nullable=False)
    nickname =                db.Column(db.String(30),      nullable=False)
    registeredOn =           db.Column(db.DateTime(),      default=datetime.now)
    password =                db.Column(db.String(24),      nullable=False)
    email =                   db.Column(db.Text,            unique=True,         nullable=False)
    imageId =                db.Column(db.Integer(),       nullable=False)
    resume =                  db.Column(db.Text,            nullable=False)
    aboutMe =                db.Column(db.Text,            nullable=False)
    address =                 db.Column(db.Text,            nullable=False)
    projectsParticipated =   db.relationship('Project',    secondary=Team,      back_populates='users')
    projectsSponsored =      db.relationship('Project',    secondary=Sponsor,   back_populates='users')


class Project(db.Model):
    __tablename__: str = 'projects'

    id =                 db.Column(db.Integer(),    primary_key=True)
    authorId =          db.Column(db.Integer(),    db.ForeignKey('users.id'))
    usersClicked =      db.Column(db.Text,         nullable=True)
    caption =            db.Column(db.String(100),  nullable=False)
    imageId =           db.Column(db.Integer(),    nullable=False)
    createdOn =         db.Column(db.DateTime(),   default=datetime.now)
    updatedOn =         db.Column(db.DateTime(),   default=datetime.now,   onupdate=datetime.now)
    neededAmount =      db.Column(db.BigInteger(), nullable=False)
    receivedAmount =    db.Column(db.BigInteger(), nullable=False)
    description =        db.Column(db.Text,         nullable=False)
    address =            db.Column(db.Text,         nullable=False)
    team =               db.relationship('User',    secondary=Team,         back_populates='projects')
    sponsors =           db.relationship('User',    secondary=Sponsor,      back_populates='projects')
