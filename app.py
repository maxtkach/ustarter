from flask import Flask
from config import Config
from tables import db
from main_blueprint import main
from project_blueprint import project
from user_blueprint import user

app = Flask(__name__)
app.secret_key = "UwU"
app.config["SQLALCHEMY_DATABASE_URI"] = Config.link
db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(user)
app.register_blueprint(main)
app.register_blueprint(project)

if __name__ == "__main__":
    app.run(debug=True)
