import functools

from flask import (Blueprint, flash, g, redirect, request, render_template, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from money_manager.db import get_db
from money_manager.auth import login_required
from country_list import countries_for_language

from datetime import datetime, timezone

bp = Blueprint("mm", __name__)

@bp.route("/", methods = ["GET"])
@login_required
def index():
    user_id = session["user_id"]
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT accounts.name, SUM(movements.amount) FROM movements JOIN accounts ON accounts.id = movements.account_id WHERE movements.user_id = %s GROUP BY accounts.name", (user_id,))
    data = cur.fetchall()
    cur.execute("SELECT SUM(amount) FROM movements WHERE user_id = %s;", (user_id, ))
    total = cur.fetchone()
    return render_template("mm/index.html", data=data, total=total)

@bp.route("/about", methods = ["GET"])
def about():
    return render_template("/about.html")


@bp.route("/income", methods = ["GET", "POST"])
@login_required
def income():
    db = get_db()
    cur = db.cursor()
    user_id = session["user_id"]
    if request.method == "POST":
        account = request.form.get("account")
        new_account = request.form.get("new_account")
        category = request.form.get("category")
        new_category = request.form.get("new_category")
        amount = float(request.form.get("amount"))
        dtime = datetime.now(timezone.utc)
        if new_account is not "":
            account = new_account
        if new_category is not "":
            category = new_category
        cur.execute("SELECT id FROM accounts WHERE name = %s;", (account, ))
        account_id = cur.fetchone()
        if account_id is None:
            cur.execute("INSERT INTO accounts (name) VALUES (%s);", (account, ))
            db.commit()
            cur.execute("SELECT id FROM accounts WHERE name = %s;", (account, ))
            account_id = cur.fetchone()[0]
        else:
            account_id = account_id[0]
        cur.execute("SELECT id FROM categories WHERE category = %s;", (category, ))
        category_id = cur.fetchone()
        if category_id is None:
            cur.execute("INSERT INTO categories (category) VALUES (%s);", (category, ))
            db.commit()
            cur.execute("SELECT id FROM categories WHERE category = %s;", (category, ))
            category_id = cur.fetchone()[0]
        else:
            category_id = category_id[0]
        cur.execute("INSERT INTO movements (user_id, account_id, mov_date, amount, category_id) VALUES (%s,%s,%s,%s,%s);", (user_id, account_id, dtime, amount, category_id))
        db.commit()
        message = "Income saved"
        flash(message)

        return redirect(url_for("index"))
    else:
        cur.execute("SELECT DISTINCT accounts.name FROM accounts JOIN movements ON movements.account_id = accounts.id WHERE movements.user_id = %s;", (user_id,))
        accounts_data = cur.fetchall()
        cur.execute("SELECT DISTINCT categories.category FROM categories JOIN movements ON movements.category_id = categories.id WHERE movements.user_id = %s ORDER BY category;", (user_id,))
        cat_data = cur.fetchall()
        total = cur.execute("SELECT SUM(amount) FROM movements WHERE user_id = %s;", (user_id, ))
        return render_template("/mm/income.html", accounts = accounts_data, categories = cat_data, total=total)

@bp.route("/payment", methods = ["GET", "POST"])
@login_required
def payment():
    db = get_db()
    cur = db.cursor()
    user_id = session["user_id"]
    if request.method == "POST":
        account = request.form.get("account")
        category = request.form.get("category")
        new_category = request.form.get("new_category")
        amount = float(request.form.get("amount"))
        dtime = datetime.now(timezone.utc)
        if new_category is not "":
            category = new_category
        cur.execute("SELECT id FROM accounts WHERE name = %s;", (account, ))
        account_id = cur.fetchone()[0]
        cur.execute("SELECT id FROM categories WHERE category = %s;", (category, ))
        category_id = cur.fetchone()
        if category_id is None:
            cur.execute("INSERT INTO categories (category) VALUES (%s);", (category, ))
            db.commit()
            cur.execute("SELECT id FROM categories WHERE category = %s;", (category, ))
            category_id = cur.fetchone()[0]
        else:
            category_id = category_id[0]
        print(amount)
        print(type(amount))
        amount = -amount
        cur.execute("INSERT INTO movements (user_id, account_id, mov_date, amount, category_id) VALUES (%s,%s,%s,%s,%s);", (user_id, account_id, dtime, amount, category_id))
        db.commit()
        message = "Payment saved"
        flash(message)
        return redirect(url_for("index"))
    else:
        cur.execute("SELECT accounts.name, SUM(movements.amount) FROM accounts JOIN movements ON movements.account_id = accounts.id WHERE movements.user_id = %s GROUP BY accounts.name;", (user_id,))
        accounts_data = cur.fetchall()
        cur.execute("SELECT DISTINCT categories.category FROM categories JOIN movements ON movements.category_id = categories.id WHERE movements.user_id = %s ORDER BY category;", (user_id,))
        cat_data = cur.fetchall()
        total = cur.execute("SELECT SUM(amount) FROM movements WHERE user_id = %s;", (user_id, ))
        return render_template("/mm/payment.html", accounts = accounts_data, categories = cat_data, total=total)

@bp.route("/movements", methods = ["GET"])
@login_required
def movements():
    db = get_db()
    cur = db.cursor()
    user_id = session["user_id"]
    cur.execute("SELECT movements.mov_date, accounts.name, categories.category, movements.amount FROM movements JOIN accounts ON accounts.id = movements.account_id JOIN categories ON categories.id = movements.category_id WHERE user_id = %s;", (user_id, ))
    data = cur.fetchall()
    return render_template("/mm/movements.html", data=data)
