import sqlite3
import psycopg2
import click
from flask import current_app, g
from flask.cli import with_appcontext
from country_list import countries_for_language

def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(
            current_app.config["DATABASE"])

    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    cur = db.cursor()
    with current_app.open_resource("schema.sql") as f:
        cur.execute(f.read())
    countries = list(dict(countries_for_language('en')).values())
    for x in countries:
        cur.execute("INSERT INTO countries (country) VALUES (%s);" , (str(x),))
        db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Database Initialized")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
