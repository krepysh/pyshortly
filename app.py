import os

from flask import Flask, url_for, redirect, render_template, request, flash

from models import db, User
from repository import repository
from services import create_short_url

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SERVER_NAME"] = os.environ.get("SERVER_NAME")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///db.sqlite"
)
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return redirect(url_for("create_url", _external=True))


@app.route("/link/new", methods=["GET", "POST"])
def create_url():
    if request.method == "POST":
        url = request.form["url"]
        link = create_short_url(url=url)
        flash(f"You have successfully created a shorten url for {link.url}")
        return redirect(url_for("link_list"))
    return render_template("new_url.html")


@app.route("/link/list")
def link_list():
    links = repository.get()
    links.sort(key=lambda x: x.created_at, reverse=True)
    return render_template("link_list.html", links=links)


@app.route("/<hash_id>")
def redirector(hash_id):
    link = repository.get(hash_id=hash_id)
    repository.update(link)
    return redirect(link.url)


@app.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
