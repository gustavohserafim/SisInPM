import functools

from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for, current_app
)

from sisinpm_app.db import get_db
from config import OAUTH_URL, REDIRECT_URI
from zenora import APIClient

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_app_request
def load_logged_in_user():
    user = session.get("user")

    if user is None:
        g.user = None
    else:
        g.user = user


@bp.route("/login", methods=("GET", "POST"))
def login():
    if g.user is None:
        return render_template("auth/login.html", oauth_url=OAUTH_URL)
    return redirect("/")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.route("/callback")
def callback():
    code = request.args.get("code")
    access_token = current_app.bot_client.oauth.get_access_token(code, REDIRECT_URI).access_token
    bearer_client = APIClient(access_token, bearer=True)
    u = bearer_client.users.get_current_user()

    session["user"] = {
        "email": u.email,
        "has_mfa_enabled": u.has_mfa_enabled,
        "id": u.id,
        "is_verified": u.is_verified,
        "username": u.username
    }

    return redirect("/")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
