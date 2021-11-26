#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# created by me60338 on 11/26/21 - 3:40 PM
# part of project flask-start
from flask import Blueprint, render_template

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
