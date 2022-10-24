import os
import time
import requests
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, redirect, url_for


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("KEY")
Bootstrap(app)

endpoint = "https://poetrydb.org"


@app.route("/")
def home():
    time.sleep(0.01)# a solution to connection reset by peer error?
    response = requests.get(f"{endpoint}/random")
    data = response.json()
    title = data[0]["title"]
    author = data[0]["author"]
    lines = data[0]["lines"]
    return render_template("index.html", title=title, author=author, lines=lines)


@app.route("/<author>")
def list_of_poems(author):
    response = requests.get(f"{endpoint}/author/{author}:abs/title")
    data = response.json()
    res = []
    for i in range(len(data)):
        try:
            res.append(data[i]["title"])
        except KeyError:
            pass
    # res = [data[i]["title"] for i in range(len(data))]
    titles = []
    [titles.append(x) for x in res if x not in titles]
    return render_template("titles.html", titles=titles, author=author)


@app.route("/<author>/<title>")
def get_poem(author, title):
    response = requests.get(f"{endpoint}/author/{author}/title,lines")
    data = response.json()
    titles = [data[i]["title"] for i in range(len(data))]
    lines = [data[i]["lines"] for i in range(len(data))]
    res = dict(zip(titles, lines))
    lines = res[title]

    return render_template("index.html", title=title, author=author, lines=lines)


if __name__ == "__main__":
    app.run(debug=True)
