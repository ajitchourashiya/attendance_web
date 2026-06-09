from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session

from models.employee import Employee

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route("/")
def login_page():
    return render_template("login.html")


@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    phone = request.form["phone"]
    password = request.form["password"]

    user = Employee.query.filter_by(
        phone=phone,
        password=password
    ).first()

    if user:

        # SAVE LOGIN SESSION
        session["user_id"] = user.id
        session["user_name"] = user.name
        session["role"] = user.role

        print("LOGIN SUCCESS")
        print(dict(session))

        return redirect("/dashboard")

    return render_template(
        "login.html",
        error="Invalid Phone or Password"
    )


@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/")