#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# created by me60338 on 11/25/21 - 3:15 PM
# part of project flaskstart
from flask import Flask, url_for, send_from_directory, request, redirect, abort
from markupsafe import escape
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path="", static_folder="quickstart-ui")


@app.route("/")
def index():
    print(f"connection from: {request.remote_addr}")
    return send_from_directory("quickstart-ui", "index.html")


@app.route("/<name>")  # name is string
def hello(name):
    return f"<h2>SA {escape(name)}!</h2>"


@app.route("/get_sum/<int:x>", methods=["GET", "POST"])  # x is integer
def get_sum(x):
    return f"<h2>2 + {x} = {2 + x}</h2>"


@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["the_file"]
    # f.save(f"uploaded/{f.filename}")
    f.save(f"uploaded/{secure_filename(f.filename)}")
    return "<h2>OK</h2><br><a href='/'>Return home</a>"


@app.route("/file_upload", methods=["POST"])
def file_upload():
    return redirect(url_for("upload"))


@app.route("/admin")
def admin():
    abort(401)


@app.errorhandler(401)
def error_401(error):
    print(error)
    return "<h1>Error 401: HOOP! Nereye müdür?<h1/>", 401
    # resp = make_response(send_from_directory("quickstart-ui", "error_401.html"))
    # resp.headers["X-HAHO"] = "GG"
    # return resp


@app.route("/json")
def json():
    return {
        "type": "JSON",
        "name": "Json object"
    }


with app.test_request_context():
    print("====TEST REQUEST START====")
    print(url_for("index"))
    print(url_for("hello", name="Selami"))
    print(url_for("get_sum", x="9"))
    print("====TEST REQUEST END====")

if __name__ == "__main__":
    print("""run with: 
     $ export FLASK_APP=quickstart
     $ export FLASK_ENV=development
     $ flask run""")
