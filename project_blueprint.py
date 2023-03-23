from flask import render_template, request, Flask, flash, redirect, url_for, Blueprint, session
from config import Config
from tables import *
from queries import *
from json import dumps, loads
from image_manager import *


project = Blueprint("project", __name__)

@project.route("/create_project", methods=("GET", "POST"))
def CreateProject():
    if request.method == "POST" and session:
        caption = request.form['caption']
        neededAmount = request.form['neededAmount']
        startBudget = request.form['startBudget']
        description = request.form['description']
        neededTeamMembers = request.form['neededTeamMembers']
        risks = request.form['risks']
        sponsorsInfo = request.form['sponsorsInfo']
        category = request.form['category_select']
        images = request.files.getlist('images_mult')
        img = request.files['images']
        if not caption:
            flash("Заголовок обов'язковий")
        elif not neededAmount:
            flash("Потрібні гроші обов'язкові")
        elif not startBudget:
            startBudget = 0
        elif not description:
            flash("Опис обов'язковий")
        elif not neededTeamMembers:
            flash("Команда обов'язкова")
        elif len(images) > 3:
            flash("Завантажуйте до 3 фоток")
        elif img.filename == '':
            flash("Картинка обов'язкова")
        elif img and allowedFile(img.filename):
            SaveImg(img)
            project = Project(caption=caption,
                              neededAmount=neededAmount,
                              receivedAmount=0,
                              startBudget=startBudget,
                              description=dumps({"description": description, "neededTeamMembers": neededTeamMembers,
                                                 "risks": risks, "sponsorsInfo": sponsorsInfo}),
                              category=category,
                              imageId=getImagesCount(),
                              mediaNames=SaveMedia(images),
                              authorId=session["id"]
                              )
            db.session.add(project)
            db.session.commit()
            return redirect(url_for("main.MainPage"))

    return render_template("project_creation.html")

@project.route("/project/<int:project_id>", methods=["GET"])
def ViewProject(project_id):
    project = ProjectQuery().GetProjectById(project_id)
    return render_template("project_page.html",
                           project=project,
                           getImageById=getImageNameById,
                           loads=loads,
                           path=UPLOAD_FOLDER,
                           getSponsors=SponsorQuery().GetSponsorsByProjectId,
                           getTeam=TeamQuery().GetTeamByProjectId,
                           len=len,
                           getMediaById=getMediaNamesByIds
                           )

@project.route("/project/<int:project_id>/edit", methods=["GET", "POST"])
def EditProject(project_id):
    project = ProjectQuery().GetProjectById(project_id)

    if request.method == "POST":
        caption = request.form['caption']
        neededAmount = request.form['neededAmount']
        startBudget = request.form['startBudget']
        description = request.form['description']
        neededTeamMembers = request.form['neededTeamMembers']
        risks = request.form['risks']
        sponsorsInfo = request.form['sponsorsInfo']
        category = request.form['category_select']
        images = request.files.getlist('images_mult')
        img = request.files['images']
        if not caption:
            flash("Заголовок обов'язковий")
        elif not neededAmount:
            flash("Потрібні гроші обов'язкові")
        elif not startBudget:
            startBudget = 0
        elif not description:
            flash("Опис обов'язковий")
        elif not neededTeamMembers:
            flash("Команда обов'язкова")
        else:
            project.caption = caption
            project.neededAmount = neededAmount
            project.startBudget = startBudget
            project.description = dumps({"description": description, "neededTeamMembers": neededTeamMembers,
                                                 "risks": risks, "sponsorsInfo": sponsorsInfo})
            project.category = category
            print(images)
            if img.filename != '':
                EditImg(img, project)
            if len(images) > 1:
                project.mediaNames = EditMedia(images, project)
            db.session.commit()
            return redirect(url_for('project.ViewProject', project_id=project_id))

    return render_template("project_edit.html",
                           project=project,
                           getImageById=getImageNameById,
                           loads=loads,
                           path=UPLOAD_FOLDER,
                           len=len,
                           getMediaById=getMediaNamesByIds
                           )
