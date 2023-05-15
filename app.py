from flask import Flask, url_for, redirect, render_template, request

from services import create_short_url

app = Flask(__name__)


@app.route("/")
def index():
    return redirect(url_for("create_url"))


@app.route("/url/new", methods=["GET", "POST"])
def create_url():
    if request.method == "POST":
        url = request.form["url"]
        link = create_short_url(url=url)  # noqa
    return render_template("new_url.html")


if __name__ == "__main__":
    app.run(debug=True)
