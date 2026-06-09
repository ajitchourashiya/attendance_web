from flask import Blueprint
from flask import render_template

from models.employee import Employee

employee_bp = Blueprint(
    "employee",
    __name__
)

@employee_bp.route("/employees")
def employees():

    data = Employee.query.all()

    return render_template(
        "employees.html",
        employees=data
    )