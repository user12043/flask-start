#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# created by me60338 on 11/26/21 - 2:36 PM
# part of project flask-start


#
#   __________              |-----------|
#  |         | --------->   | BLUEPRINT | ------------> VIEW
#  |         |              |           | ------------> VIEW
#  |         |              |___________|
#  | CLIENT  |
#  |         |               |-----------|
#  |         |  --------->   | BLUEPRINT | ------------> VIEW
#  |         |               |           | ------------> VIEW
#  |_________|               |___________|
import functools

from flask import (
    Blueprint, request, redirect, url_for, flash, session, g, render_template
)
from werkzeug.security import generate_password_hash, check_password_hash

from app.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username or not password:
            error = "Username and password required"

        if error is None:
            try:
                db.execute("INSERT INTO user (username, password) VALUES (?, ?)",
                           (username, generate_password_hash(password)))
                db.commit()
            except db.IntegrityError:
                error = f"{username} is already exist"
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    # return send_from_directory("auth", "register.html")
    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute("SELECT id, username, password FROM user WHERE username = ?", (username,)).fetchone()
        if user is None or not check_password_hash(user["password"], password):
            error = "Invalid username or password"

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))
        flash(error)

    # return send_from_directory("auth", "login.html")
    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))  # url for view "login" under blueprint "auth"
        return view(**kwargs)

    return wrapped_view()
