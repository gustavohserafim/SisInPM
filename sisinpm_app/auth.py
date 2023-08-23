import functools
from sisinpm_app import helper, controller
from flask import (Blueprint, g, redirect, render_template, request, session, url_for, flash)
from config import OAUTH_URL

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user = session.get("user")
    if user is None:
        g.user = None
    else:
        g.user = user


@bp.route("/register", methods=("GET", "POST"))
def register():
    tipo_graduacoes = controller.AuthController.get_graduacoes()

    if request.method == "POST":
        data = request.form
        create = controller.UserController.create(data.get('email'), data.get('password'), data.get('qra'),
                                                  data.get('graduacao'), data.get('estagio'))
        if create:
            return redirect("/")
        flash("Email já cadastrado.")
        return render_template("auth/register.html", tipo_graduacoes=tipo_graduacoes)
    else:
        return render_template("auth/register.html", tipo_graduacoes=tipo_graduacoes)


@bp.route("/login", methods=("GET", "POST"))
def login():
    if g.user is None:
        if request.method == "GET":
            return render_template("auth/login.html")
        elif request.method == "POST":
            data = request.form
            auth = controller.AuthController.login(data.get('email'), data.get('password'))
            if auth:
                session["user"] = auth
            else:
                flash("Email e/ou senha incorreto(s).")
                return render_template("auth/login.html")
    return redirect("/")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.route("/callback")
def callback():
    code = request.args.get("code")
    return helper.get_access_token(code)
    # return redirect("/")
