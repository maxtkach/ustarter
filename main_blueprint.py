from flask import render_template, request, Flask, flash, redirect, url_for, Blueprint, session
from queries import *
from json import dumps, loads
from random import choice
from image_manager import UPLOAD_FOLDER, getImageNameById

main = Blueprint("main", __name__)

@main.route("/")
def MainPage():
    print(session)
    projects = ProjectQuery().GetProjects()
    project1 = choice(projects)
    projects.remove(project1)
    project2 = choice(projects)
    projects.remove(project2)
    project3 = choice(projects)
    projects.remove(project3)

    print(UserQuery().GetUserById(1).notifications)
    latestProjects = ProjectQuery().GetLatestProjects()
    return render_template("index.html",
                           project1=project1,
                           project2=project2,
                           project3=project3,
                           path=UPLOAD_FOLDER,
                           getImageById=getImageNameById,
                           loads=loads,
                           latestProjects=latestProjects,
                           getUserById=UserQuery().GetUserById
                           )
