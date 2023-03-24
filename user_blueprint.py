from flask import render_template, request, Flask, flash, redirect, url_for, Blueprint, session
from config import Config
from tables import *
from queries import *
from image_manager import *
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

def Identify(id, password):
    user = UserQuery().GetUserById(id)
    return user and user.id == id and user.password == password

# WARNING: should be removed or redirected to ShowProfile
@user.route("/profile")
def Profile():
    if Identify(session["id"], session["password"]):
        return redirect(url_for("user.ShowProfile", id=int(session["id"])))
    return redirect(url_for("Login"))
    # return render_template("profile.html") #, userName=session["email"] if session["email"] else "Unknown")

@user.route("/profile/<int:id>")
def ShowProfile(id):
    user = UserQuery().GetUserById(id) #session["id"])
    return render_template("profile.html",
                           fullName=user.name,
                           email=user.email,
                           aboutMe=user.aboutMe,
                           resume=user.resume,
                           image_path=f"{UPLOAD_FOLDER_AVATARS}/{getImageNameById(id, UPLOAD_FOLDER_AVATARS)}"
                           )# + " " + user.surname

@user.route("/profile/<int:id>_edit", methods=["GET", "POST"])
def EditProfile(id):
    if session:
        user = UserQuery().GetUserById(session["id"])
        if user.email == session["email"] and user.password == session["password"]:
            if session["id"] == id:
                if request.method == "GET":
                    return render_template("user_edit.html", user=user, loads=loads)
                elif request.method == "POST":
                    img = request.files["avatar"]
                    # if request["name"] and request["surname"] and request["avatar"]
                    user.name = request.form["name"]
                    # UserQuery().GetUserById(session["id"]).surname = request.form["surname"]
                    user.aboutMe = request.form["aboutMe"]
                    user.address = request.form["address"]
                    user.resume = request.form["resume"]
                    if img and allowedFile(img.filename):
                        if getImageNameById(session["id"], UPLOAD_FOLDER_AVATARS):
                            print("(here)")
                            EditImg(img, user, UPLOAD_FOLDER_AVATARS)
                        else:
                            print("(here2)")
                            SaveImg(img, UPLOAD_FOLDER_AVATARS, session["id"])
                    user.social_media = dumps({"telegram": request.form["telegram"], "tiktok": request.form["tiktok"],
                                               "instagram": request.form["instagram"], "twitter": request.form["twitter"]})

                    db.session.commit()
                    return redirect(f"../../profile/{id}")
            else:
                # Not authorized
                # return redirect(f"../profile/{user.id}");
                return redirect(f"../../profile/{id}")
        else:
            return redirect(url_for("user.Logout"))
    return redirect(url_for("user.Login")) # render_template("profile.html")

@user.route("/signup")
def SignupPage():
    return render_template("signup.html")

@user.route("/logout")
def Logout():
    session.clear()
    return redirect(url_for("user.SignupPage"))

@user.route("/login", methods=["POST"])
def Login():
    # Should be try...except used or Flask will handle incorrect requests itself?
    print("Recieved POST request for login from", request.remote_addr)
    if IsEmailValid(request.form["email"]) and IsPasswordValid(request.form["password"]): # not necessary
        loginAttempt = UserQuery().GetUserByEmail(request.form["email"])  #db.session.query(User).filter(User.email == request.form["email"]).first() # print(db.session.query(User).first())
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
            # WARNING: should be checked if user already exists
            newUser = User()
            newUser.name = request.form["username"]
            newUser.nickname = request.form["nickname"]
            newUser.email = request.form["email"]
            newUser.password = request.form["password"]

            newUser.resume = ""
            newUser.aboutMe = ""
            newUser.address = ""

            session["email"] = newUser.email
            session["password"] = newUser.password

            db.session.add(newUser)
            db.session.commit()

            session["id"] = UserQuery().GetUserByEmail(request.form["email"]).id
        else:
            return redirect(url_for("user.SignupPage", error="Please fill out all values"))
        return redirect(url_for("user.EditProfile", id=session["id"])) #url_for("user.Profile") # Welcome message?
    else:
        return redirect(url_for("user.SignupPage", error="Please fill out all values"))
        # return render_template("signup.html", error="Please fill out all values")
