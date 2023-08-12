from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)

from sisinpm_app.auth import login_required

bp = Blueprint('core', __name__, url_prefix='/')


@bp.route('', methods=('GET', 'POST'))
@login_required
def index():
    print(f"g:{g.user}")
    return str(g.user)
