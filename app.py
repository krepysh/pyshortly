import os
from datetime import datetime

from flask import Flask, url_for, redirect, render_template, request, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from flask_migrate import Migrate
from sqlalchemy import select
from werkzeug.security import check_password_hash, generate_password_hash

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
migrate = Migrate(app=app, db=db)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_name) -> User:
    stmt = select(User).where(User.username == user_name)
    user = db.session.scalar(stmt)
    return user


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
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("register.html")


@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = load_user(username)
        if user and check_password_hash(user.password, password):
            previous_login = (
                user.last_login.strftime("%Y-%m-%d %H:%M:%S")
                if user.last_login
                else "Never"
            )
            flash(
                f"You successfully logged-in. Your last login was on: {previous_login}"
            )
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("index"))
        flash("Wrong credentials")
    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    flash("You logged out.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
