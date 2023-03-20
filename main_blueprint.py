from flask import render_template, request, Flask, flash, redirect, url_for, Blueprint
from config import Config
from tables import *
from queries import *
from json import dumps, loads

main = Blueprint("main", __name__)

@main.route("/")
def MainPage():
    return render_template("index.html")
