from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

Team = db.Table(
    "user_project_team",
    db.Column('id', db.Integer(),       primary_key=True),
    db.Column('userId', db.Integer(),   db.ForeignKey('users.id')),
    db.Column('projectId', db.Integer(),   db.ForeignKey('projects.id')),
    db.Column('role', db.String(40),  nullable=False)
)

Sponsor = db.Table(
    'user_project_helper',
    db.Column('id', db.Integer(),       primary_key=True),
    db.Column('userId', db.Integer(),      db.ForeignKey('users.id')),
    db.Column('projectId', db.Integer(),      db.ForeignKey('projects.id')),
    db.Column('money', db.BigInteger(),   nullable=False)
)


class User(db.Model):
    __tablename__: str = 'users'

    id =                      db.Column(db.Integer(),       primary_key=True)
    name =                    db.Column(db.String(102),     nullable=False)
    nickname =                db.Column(db.String(30),      nullable=True)
    registeredOn =           db.Column(db.DateTime(),      default=datetime.now)
    password =                db.Column(db.String(24),      nullable=False)
    email =                   db.Column(db.Text,            unique=True,         nullable=False)
    imageId =                db.Column(db.Integer(),       nullable=True)
    resume =                  db.Column(db.Text,            nullable=True)
    aboutMe =                db.Column(db.Text,            nullable=True)
    address =                 db.Column(db.Text,            nullable=True)
    projectsParticipated =   db.relationship('Project',    secondary=Team,      backref=db.backref('users_members'))
    projectsSponsored =      db.relationship('Project',    secondary=Sponsor,   backref=db.backref('users_sponsors'))


class Project(db.Model):
    __tablename__: str = 'projects'

    id =                 db.Column(db.Integer(),    primary_key=True)
    authorId =          db.Column(db.Integer(),    db.ForeignKey('users.id'))
    usersClicked =      db.Column(db.Text,         nullable=True)
    category =          db.Column(db.Text,         nullable=False)
    caption =            db.Column(db.String(100),  nullable=False)
    imageId =           db.Column(db.Integer(),    nullable=False)
    mediaNames =        db.Column(db.String(31),   nullable=True)
    createdOn =         db.Column(db.DateTime(),   default=datetime.now)
    updatedOn =         db.Column(db.DateTime(),   default=datetime.now,   onupdate=datetime.now)
    neededAmount =      db.Column(db.BigInteger(), nullable=False)
    receivedAmount =    db.Column(db.BigInteger(), nullable=True)
    startBudget =       db.Column(db.Integer(), nullable=False)
    description =        db.Column(db.Text,         nullable=False)
    address =            db.Column(db.Text,         nullable=True)
    #team =               db.relationship('User',    secondary=Team,         backref=db.backref('projects'))
    #sponsors =           db.relationship('User',    secondary=Sponsor,      backref=db.backref('projects'))
