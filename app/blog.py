#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# created by me60338 on 11/26/21 - 3:40 PM
# part of project flask-start
from flask import (
    Blueprint, render_template, request, flash, g, redirect, url_for, abort
)

from app.auth import login_required
from app.db import get_db

bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("blog/index.html")


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title required"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id)"
                " VALUES (?, ?, ?)",
                (title, body, g.user["id"])
            )
            db.commit()
            return redirect(url_for("blog.index"))
    return render_template("blog/create.html")


def get_post(post_id, check_author=True):
    post = get_db().execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " WHERE p.id = ?",
        (post_id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post {post_id} not found")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)
    return post


@bp.route("/<int:post_id>/update")
@login_required
def update(post_id):
    post = get_post(post_id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["title"]
        error = None

        if not title:
            error = "Title required"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ?"
                " WHERE id = ?",
                (title, body, post_id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html")


@bp.route("/<int:post_id>/delete", methods=("POST",))
@login_required
def delete(post_id):
    get_post(post_id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (post_id,))
    db.commit()
    return redirect(url_for("blog.index"))
