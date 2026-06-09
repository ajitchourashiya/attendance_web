from flask import Blueprint
from flask import render_template

from models.role import Role

role_bp = Blueprint(
    "role",
    __name__
)

@role_bp.route("/roles")
def roles():

    data = Role.query.all()

    return render_template(
        "roles.html",
        roles=data
    )