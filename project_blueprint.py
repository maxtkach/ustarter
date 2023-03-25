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
        address = request.form['address_select']
        images = request.files.getlist('images_mult')
        img = request.files['images']
        if not caption:
            flash("Заголовок обов'язковий")
        elif ProjectQuery().GetProjectByCaption(caption):
            flash("Проект з таким заголовком вже є")
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
        elif not category:
            flash("Категорія обов'язкова")
        elif not address:
            flash("Адреса обов'язкова")
        elif img and allowedFile(img.filename):
            project = Project(caption=caption,
                              neededAmount=neededAmount,
                              receivedAmount=0,
                              startBudget=startBudget,
                              description=dumps({"description": description, "neededTeamMembers": neededTeamMembers,
                                                 "risks": risks, "sponsorsInfo": sponsorsInfo}),
                              category=category,
                              address=address,
                              authorId=session["id"]
                              )
            db.session.add(project)
            db.session.commit()
            project = ProjectQuery().GetProjectByCaption(caption)
            #user = UserQuery().GetUserById(session["id"])
            #team = ProjectTeam()
            #team.project = project
            #team.user = user
            #team.role = "Автор"
            #db.session.add(team)
            #db.session.commit()
            SaveImg(img, img_id=project.id)
            project.mediaNames = SaveMedia(images, img_id=project.id)
            return redirect(url_for('project.ViewProject', project_id=project.id))

    return render_template("project_creation.html")

@project.route("/project/<int:project_id>", methods=["GET"])
def ViewProject(project_id):
    project = ProjectQuery().GetProjectById(project_id)
    usersClicked = project.usersClicked
    if usersClicked is not None:
        if usersClicked == "":
            project.usersClicked = str(session['id'])
            db.session.commit()
        else:
            usersClicked = [int(e) for e in usersClicked.split(" ")]
            if session['id'] not in usersClicked:
                usersClicked.append(session["id"])
                project.usersClicked = " ".join([str(i) for i in usersClicked])
                db.session.commit()
    else:
        project.usersClicked = str(session['id'])
        db.session.commit()

    return render_template("project_page.html",
                           project=project,
                           getImageById=getImageNameById,
                           loads=loads,
                           path=UPLOAD_FOLDER,
                           path_avatar=UPLOAD_FOLDER_AVATARS,
                           len=len,
                           getMediaById=getMediaNamesByIds,
                           getUserById=UserQuery().GetUserById
                           )

@project.route("/project/<int:project_id>_edit", methods=["GET", "POST"])
def EditProject(project_id):
    project = ProjectQuery().GetProjectById(project_id)

    if request.method == "POST" and session:
        if project.authorId != session["id"]:
            return redirect(url_for('project.ViewProject', project_id=project_id))
        caption = request.form['caption']
        neededAmount = request.form['neededAmount']
        startBudget = request.form['startBudget']
        description = request.form['description']
        neededTeamMembers = request.form['neededTeamMembers']
        risks = request.form['risks']
        sponsorsInfo = request.form['sponsorsInfo']
        category = request.form['category_select']
        address = request.form['address_select']
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
        elif not category:
            flash("Категорія обов'язкова")
        elif not address:
            flash("Адреса обов'язкова")
        else:
            project.caption = caption
            project.neededAmount = neededAmount
            project.startBudget = startBudget
            project.description = dumps({"description": description, "neededTeamMembers": neededTeamMembers,
                                                 "risks": risks, "sponsorsInfo": sponsorsInfo})
            project.category = category
            project.address = address
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

@project.route("/project/<int:project_id>_delete", methods=["POST"])
def DeleteProject(project_id):
    project = ProjectQuery().GetProjectById(project_id)
    if session["id"] == project.authorId:
        db.session.delete(project)
        db.session.commit()
    return redirect(url_for("main.MainPage"))

@project.route("/project/<int:project_id>/apply_team_member", methods=["POST"])
def ApplyTeamMember(project_id):
    project = ProjectQuery().GetProjectById(project_id)
    applications = loads(UserQuery().GetUserById(project.authorId).notifications)
    for a in applications:
        try:
            if a["user_id"] == session["id"]:
                return redirect(url_for('project.ViewProject', project_id=project_id))
        except KeyError:
            continue
    for t in project.team:
        print(t.userId)
        if t.userId == session["id"] or session["id"] == project.authorId:
            return redirect(url_for('project.ViewProject', project_id=project_id))
    phone_number = request.form['telephone_number']
    message = request.form['message']
    role = request.form['role']
    if not phone_number:
        flash("Уведіть номер телефону")
        return redirect(url_for('project.ViewProject', project_id=project_id))
    elif not message:
        flash("Уведіть текст повідомлення")
    elif not role:
        flash("Уведіть спеціальність")
    else:
        author = UserQuery().GetUserById(project.authorId)
        if not author.notifications:
            author.notifications = dumps([{"telephone_number": phone_number, "message": message, "role": role,
                                           "user_id": session['id'], "project_id": project_id,
                                           "type": "Заявка до команди"}])
        else:
            loaded_notifications = loads(author.notifications)
            loaded_notifications.append({"telephone_number": phone_number, "message": message, "role": role,
                                           "user_id": session['id'], "project_id": project_id,
                                           "type": "Заявка до команди"})
            author.notifications = dumps(loaded_notifications)
        db.session.commit()
        return redirect(url_for('project.ViewProject', project_id=project_id))


@project.route("/project/<int:project_id>/become_sponsor", methods=["POST"])
def BecomeSponsor(project_id):
    project = ProjectQuery().GetProjectById(project_id)
