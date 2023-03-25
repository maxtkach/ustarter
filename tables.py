from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
# from app import db
# db = SQLAlchemy() # SQLAlchemy(app)?
db = SQLAlchemy()

class ProjectTeam(db.Model):
    __tablename__ = 'user_project_team'
    id =           db.Column(db.Integer(),       primary_key=True)
    userId =       db.Column(db.Integer(),      db.ForeignKey('users.id'))
    projectId =    db.Column(db.Integer(),      db.ForeignKey('projects.id'))
    role =         db.Column(db.String(40),  nullable=False)

    user =         db.relationship('User', back_populates='projectsParticipated')
    project =      db.relationship('Project', back_populates='team')

class UserSponsor(db.Model):
    __tablename__ = 'user_project_helper'
    id =           db.Column(db.Integer(),       primary_key=True)
    userId =       db.Column(db.Integer(),      db.ForeignKey('users.id'))
    projectId =    db.Column(db.Integer(),      db.ForeignKey('projects.id'))
    money =        db.Column(db.BigInteger(),   nullable=False)

    user =         db.relationship('User', back_populates='projectsSponsored')
    project =      db.relationship('Project', back_populates='sponsors')



class User(db.Model):
    __tablename__: str = 'users'

    id =                      db.Column(db.Integer(),       primary_key=True)
    name =                    db.Column(db.String(102),     nullable=False)
    nickname =                db.Column(db.String(30),      nullable=True)
    registeredOn =           db.Column(db.DateTime(),      default=datetime.now)
    password =                db.Column(db.String(24),      nullable=False)
    email =                   db.Column(db.Text,            unique=True,         nullable=False)
    resume =                  db.Column(db.Text,            nullable=True)
    aboutMe =                db.Column(db.Text,            nullable=True)
    notifications =          db.Column(db.Text,            nullable=True)
    social_media =           db.Column(db.Text,            nullable=True)
    address =                 db.Column(db.Text,            nullable=True)
    projectsParticipated =   db.relationship('ProjectTeam', back_populates='user')
    projectsSponsored =      db.relationship('UserSponsor', back_populates='user')


class Project(db.Model):
    __tablename__: str = 'projects'

    id =                 db.Column(db.Integer(),    primary_key=True)
    authorId =          db.Column(db.Integer(),    nullable=True)
    usersClicked =      db.Column(db.Text,         nullable=True)
    category =          db.Column(db.Text,         nullable=False)
    caption =            db.Column(db.String(100),  nullable=False)
    mediaNames =        db.Column(db.String(31),   nullable=True)
    createdOn =         db.Column(db.DateTime(),   default=datetime.now)
    updatedOn =         db.Column(db.DateTime(),   default=datetime.now,   onupdate=datetime.now)
    neededAmount =      db.Column(db.BigInteger(), nullable=False)
    receivedAmount =    db.Column(db.BigInteger(), nullable=True)
    startBudget =       db.Column(db.Integer(), nullable=False)
    description =        db.Column(db.Text,         nullable=False)
    address =            db.Column(db.Text,         nullable=True)
    team =               db.relationship('ProjectTeam', back_populates='project')
    sponsors =           db.relationship('UserSponsor', back_populates='project')
