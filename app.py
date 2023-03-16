from flask import *

app = Flask(__name__)
app.secret_key = "UwU"
# app.config["SQLALCHEMY_DATABSE_URI"] = "sqlite:///db.sqlite3"

# db = SQLAlchemy(app)
# classes here...

@app.route("/")
def MainPage():
    return render_template("index.html")

if __name__ == "__main__": app.run(debug=True)