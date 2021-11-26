#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# created by me60338 on 11/26/21 - 11:03 AM
# part of project flask-start

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource("schema.sql") as file:
        db.executescript(file.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Database initialized")


def register_db_things(app):
    app.teardown_appcontext(close_db)  # close db when cleaning up after response
    app.cli.add_command(init_db_command)
