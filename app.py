from flask import render_template, request, Flask, flash, redirect, url_for
from ustarter.ustarter.config import Config
from flask_sqlalchemy import SQLAlchemy
from ustarter.ustarter.tables import *
from ustarter.ustarter.queries import *
from json import dumps, loads

app = Flask(__name__)
app.secret_key = "UwU"
app.config["SQLALCHEMY_DATABASE_URI"] = Config.link
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/")
def MainPage():
    #print(ProjectQuery().GetProjectById(4).caption)
    return render_template("index.html")

@app.route("/create_project", methods=("GET", "POST"))
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

@app.route("/profile")
def Profile():
    return render_template("profile.html")

if __name__ == "__main__":
    app.run(debug=True)
