import functools

from flask import (
    Blueprint, request, redirect, render_template, g, session, url_for, flash
)
from werkzeug.security import (
    check_password_hash, generate_password_hash
)

from joke_share.db import get_db
from joke_share.auth.helpers import (
    is_valid_email, is_valid_username, is_valid_passowrd
)
bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    """A view which handles requests regarding user registeration"""

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        db = get_db()
        email_exists = db.execute("SELECT email FROM User WHERE email = ?", (email, ))
        uname_esists = db.execute("SELECT username FROM User WHERE username = ?", (username, ))

        if not all([name, email, username, password]):
            flash("All fields are required", category="error")
        elif not is_valid_email(email):
            flash("Invalid email.", category="error")
        elif not is_valid_username(username):
            flash("Invalid username", category="error")
        elif not is_valid_passowrd(password):
            flash("Weak password:", category="error")
        elif email_exists.fetchone():
            flash("Email already exists", category="error")
        elif uname_esists.fetchone():
            flash("Username already exists", category="error")
        else:
            q = """
            INSERT INTO User(name, email, username, password)
            VALUES(?, ?, ?, ?)
            """
            phash = generate_password_hash(password)
            db.execute(q, (name, email, username, phash))
            db.commit()
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html")
    

@bp.route("/login", methods=["GET", "POST"])
def login():
    """A view to support user login."""

    if request.method == "POST":
        handle = request.form.get("handle")
        password = request.form.get("password")
        db = get_db()
        data = db.execute("SELECT username, password FROM User"
                          " WHERE username = ? OR email = ?",
                          (handle, handle)).fetchone()
        if not all([handle, password]):
            flash("All fields are required", "error")
        elif not data:
            flash("No such username or email exists", "error")
        elif not check_password_hash(data["password"], password):
            flash("Wrong password", "error")
        else:
            session.clear()
            session["username"] = data["username"]
            return redirect(url_for("dummy")) # Temporary
    return render_template("auth/login.html")


def login_required(func):
    @functools.wraps(func)
    def func_with_login(*args, **kwargs):
        if session.get("username") is not None:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("auth.login"))
    return func_with_login


