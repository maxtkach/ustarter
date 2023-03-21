from flask import render_template, request, Flask, flash, redirect, url_for, Blueprint
from config import Config
from tables import *
from queries import *
from json import dumps, loads

user = Blueprint("user", __name__)

@user.route("/profile")
def Profile():
    return render_template("profile.html")

@user.route("/signup")
def SignupPage():
    return render_template("signup.html")
