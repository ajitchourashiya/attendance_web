from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect

from models.employee import Employee

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)

@dashboard_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/")

    user = Employee.query.get(
        session["user_id"]
    )

    return render_template(
        "dashboard.html",
        user=user,
        role=user.role
    )