from flask import *
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "UwU"
app.config["SQLALCHEMY_DATABASE_URI"] = Config.link
db = SQLAlchemy(app)

@app.route("/")
def MainPage():
    return render_template("index.html")

@app.route("/create_project")
def CreateProject():
    return render_template("project_creation.html")

@app.route("/profile")
def Profile():
    return render_template("profile.html")

if __name__ == "__main__":
    app.run(debug=True)
