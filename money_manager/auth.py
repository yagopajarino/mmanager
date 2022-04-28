import functools

from flask import (Blueprint, flash, g, redirect, request, render_template, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from money_manager.db import get_db
from country_list import countries_for_language

bp = Blueprint("auth", __name__, url_prefix="/auth")

def get_countries():
    # countries_for_language returns a list of tuples now, might be changed to an OrderedDict
    countries = dict(countries_for_language('en'))
    return countries.values()

@bp.route("/register", methods = ["GET", "POST"])
def register():
    countries = get_countries()
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        FirstName = request.form["FirstName"]
        LastName = request.form["LastName"]
        birth = request.form["birth"]
        country = request.form["country"]
        db = get_db()
        cur = db.cursor()
        error = None
        cur.execute("SELECT * FROM users WHERE username = %s;", (username,))
        if cur.fetchone() is not None:
            error = "User {} is already registered".format(username)
        cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
        if cur.fetchone() is not None:
            error = "Email {} is already registered".format(email)

        if error is None:
            cur.execute("SELECT id FROM countries WHERE country = %s", (country,))
            country_id = cur.fetchone()
            cur.execute("INSERT INTO users (username, password, email, FirstName, LastName, birth, country) VALUES (%s, %s, %s, %s, %s, %s, %s);", (username, generate_password_hash(password), email, FirstName, LastName, birth, country_id[0],))
            db.commit()
            return redirect(url_for("auth.login"))
        
        flash(error)
    else:
        return render_template("auth/register.html", countries = countries)

@bp.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s OR email = %s;", (username, username,))
        user = cur.fetchone()
        error = None
        if user is None:
            error = "Incorrect email or username"
        elif not check_password_hash(user[-1], password):
            error = "Incorrect password"
        
        if error is None:
            session.clear()
            session["user_id"] = user[0]
            session["user_name"] = user[3]
            return redirect(url_for("index"))
        flash(error)
    return render_template("auth/login.html")

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    db = get_db()
    cur = db.cursor()
    if user_id is None:
        g.user = None
    else:
        cur.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
        g.user = cur.fetchone()

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        
        return view(**kwargs)
    
    return wrapped_view