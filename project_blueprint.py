from flask import render_template, request, Flask, flash, redirect, url_for, Blueprint
from config import Config
from tables import *
from queries import *
from json import dumps, loads

project = Blueprint("project", __name__)

@project.route("/create_project", methods=("GET", "POST"))
def CreateProject():
    if request.method == "POST":
        caption = request.form['caption']
        neededAmount = request.form['neededAmount']
        startBudget = request.form['startBudget']
        description = request.form['description']
        neededTeamMembers = request.form['neededTeamMembers']
        if not caption:
            flash("Заголовок обов'язковий")
        elif not neededAmount:
            flash("Потрібні гроші обов'язкові")
        elif not startBudget:
            startBudget = 0
        elif not description:
            flash("Опис обов'язковий")
        elif not neededTeamMembers:
            flash("Команда обов'язковий")
        else:
            project = Project(caption=caption,
                              neededAmount=neededAmount,
                              receivedAmount=0,
                              startBudget=startBudget,
                              description=dumps({"description": description, "neededTeamMembers": neededTeamMembers}),
                              category="Постраждалі",
                              imageId=1,
                              )
            session = db.session
            session.add(project)
            db.session.commit()
            return redirect(url_for("MainPage"))

    return render_template("project_creation.html")

@project.route("/project/<int:project_id>", methods=["GET"])
def ViewProject():
    return render_template("project_page.html")
