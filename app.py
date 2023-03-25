from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from tables import db

app = Flask(__name__)
app.secret_key = "UwU"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db" # Config.link
# db = SQLAlchemy(app)
db.init_app(app)
with app.app_context():
    db.create_all()

from main_blueprint import main
from project_blueprint import project
from user_blueprint import user

app.register_blueprint(user)
app.register_blueprint(main)
app.register_blueprint(project)

if __name__ == "__main__":
    app.run(debug=True)
