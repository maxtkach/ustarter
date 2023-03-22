from flask import render_template, request, Flask, flash, redirect, url_for, Blueprint, session
from config import Config
from tables import *
from queries import *
from json import dumps, loads

user = Blueprint("user", __name__)

def IsEmailValid(email):
    return False if '@' not in email or '.' not in email or len(email) < 4 else True

def IsPasswordValid(password):
    # WARNING: max and min password size should be like in DB
    return len(password) > 3 and len(password) < 24

def IsNameValid(name):
    # WARNING: max and min name size should be like in DB
    return len(name) > 2 and len(name) < 100

def IsNicknameValid(name):
    # WARNING: max and min name size should be like in DB
    return len(name) > 3 and len(name) < 30

# WARNING: should be removed or redirected to ShowProfile
@user.route("/profile")
def Profile():
    return render_template("profile.html")

@user.route("/profile/<int:id>")
def ShowProfile(id):
    return render_template("profile.html")

@user.route("/signup")
def SignupPage():
    return render_template("signup.html")

@user.route("/login", methods=["POST"])
def Login():
    # Should be try...except used or Flask will handle incorrect requests itself?
    print("Recieved POST request for login from", request.remote_addr)
    if IsEmailValid(request.form["email"]) and IsPasswordValid(request.form["password"]): # not necessary
        loginAttempt = db.session.query(User).filter(User.email == request.form["email"]).first() # print(db.session.query(User).first())
        print("Searching through", UserQuery().GetUsers())
        if not loginAttempt or loginAttempt.password != request.form["password"]:
            print(loginAttempt)
            return render_template("signup.html", error="Invalid credentials")

        session["email"] = loginAttempt.email
        session["password"] = loginAttempt.password
        session["id"] = loginAttempt.id
        return redirect(url_for("user.Profile"))# return url_for("user.Profile") # Should be redirect
    else:
        return redirect(url_for("user.SignupPage", error="Please fill out all values"))
        # return render_template("signup.html", error="Please fill out all values") # Should be redirect

@user.route("/register", methods=["POST"])
def Register():
    # Should be try...except used or Flask will handle incorrect requests itself?
    print("Recieved POST request for registration from", request.remote_addr)
    if IsEmailValid(request.form["email"]) and IsPasswordValid(request.form["password"]):
        if IsNameValid(request.form["username"]) and IsNicknameValid(request.form["nickname"]): # WARNING: defference between name and nickname
            newUser = User()
            newUser.name = request.form["username"]
            newUser.nickname = request.form["nickname"]
            newUser.email = request.form["email"]
            newUser.password = request.form["password"]

            newUser.resume = ""
            newUser.aboutMe = ""
            newUser.address = ""

            db.session.add(newUser)
            db.session.commit()
        else:
            return redirect(url_for("user.SignupPage", error="Please fill out all values"))
        return redirect(url_for("user.Profile")) #url_for("user.Profile") # Welcome message?
    else:
        return redirect(url_for("user.SignupPage", error="Please fill out all values"))
        # return render_template("signup.html", error="Please fill out all values")
