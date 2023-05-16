import os

from flask import Flask, url_for, redirect, render_template, request, flash

from repository import repository
from services import create_short_url

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")


@app.route("/")
def index():
    return redirect(url_for("create_url"))


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
    return render_template("link_list.html", links=links)


if __name__ == "__main__":
    app.run(debug=True)
