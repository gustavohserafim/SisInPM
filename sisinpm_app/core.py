from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)

from sisinpm_app.auth import login_required
from sisinpm_app.controller import UserController, CoreController

bp = Blueprint("core", __name__, url_prefix="/")


@bp.route("", methods=("GET", "POST"))
@login_required
def index():
    from config import DB_USER, DB_PASS, DB_HOST, DB_SCHEMA
    print("VARS:" + DB_USER, DB_PASS, DB_HOST, DB_SCHEMA)
    return render_template("core/index.html")


@bp.route("/avaliar", methods=["GET", "POST"])
@login_required
def avaliar():
    if request.method == "POST":
        avaliacao_data = request.form

        if CoreController.avaliar(g.user.get("id"), avaliacao_data.get("avaliado"), avaliacao_data.get("qualidades"),
                                  avaliacao_data.get("novidades"), avaliacao_data.get("nota"),
                                  avaliacao_data.get("policial1"), avaliacao_data.get("policial2")):
            flash("Avaliação cadastrada com sucesso!")
        else:
            flash("Erro ao avaliar!")
        return render_template("core/avaliar.html", estagios=UserController.get_estagios(),
                               policiais=UserController.get_policiais())
    else:
        return render_template("core/avaliar.html", estagios=UserController.get_estagios(),
                               policiais=UserController.get_policiais())


@bp.route("/healthcheck", methods=["GET"])
def health_check():
    return "ok", 200
