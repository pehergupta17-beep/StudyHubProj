from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/about")
def about():
    return render_template("about.html")

@main.route("/deadlines")
def deadlines():
    return render_template("deadlines.html")

@main.route("/pomodoro")
def pomodoro():
    return render_template("pomodoro.html")

@main.route("/quotes")
def quotes():
    return render_template("quotes.html")

@main.route("/todo")
def todo():
    return render_template("todo.html")

@main.route("/calendar")
def calendar():
    return render_template("calendar.html")