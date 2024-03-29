from flask import (
    Blueprint, request, redirect, render_template, g, session, url_for, flash
)

from joke_share.auth.auth import login_required
from joke_share.db import get_db

bp = Blueprint("jokes", __name__, url_prefix="/jokes")


@bp.route("/")
def jokes():
    """Displays initial jokes page"""
    return render_template("jokes/jokes.html")


@bp.route("/get")
def get_jokes():
    """Returns a JSON data containing jokes"""

    count = request.args.get("count", 10, int)
    offset = request.args.get("offset", 0, int)
    sortby = request.args.get("sortby", "time")

    if sortby not in ["time", "like", "rating"] or count < 0 or offset < 0:
        return {"error": "Invalid parameters"}, 400

    db = get_db()
    q = db.execute("SELECT COUNT(*) AS count FROM joke")
    n_jokes = q.fetchone()["count"]
    if offset >= n_jokes:
        return {"error": "No jokes remaining"}, 401

    sorter_col = {
        "tiem": "posting_date",
        "like": "likes",
        "rating": "rating"
    }.get(sortby)

    q = """
        SELECT Joke.id AS id, title, content, posting_date, likes, rating, username AS poster
        FROM Joke JOIN User ON Joke.poster_id = User.id
        ORDER BY ? LIMIT ? OFFSET ?
    """
    data = db.execute(q, (sorter_col, count, offset)).fetchall()
    response = {
        "jokes": data,
        "count": len(data),
        "next_offset": offset + len(data),
        "remaining": n_jokes - offset - len(data)
    }
    with open("logs.log") as f:
        print(response, file=f)
    return response
