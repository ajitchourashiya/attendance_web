from flask import Blueprint, jsonify, session
from models.attendance import Attendance
from models.employee import Employee

view_attendance_bp = Blueprint("view_attendance", __name__)

@view_attendance_bp.route("/api/view-attendance")
def view_attendance():

    user_id = session.get("user_id")
    role = session.get("role")

    if not user_id:
        return jsonify({
            "success": False,
            "message": "Not logged in"
        })

    # =========================
    # 🛡️ ADMIN → ALL DATA
    # =========================
    if role == "admin":

        records = Attendance.query.all()

    # =========================
    # 👤 USER → ONLY OWN DATA
    # =========================
    else:

        records = Attendance.query.filter_by(student_id=user_id).all()

    data = []

    for a in records:

        user = Employee.query.filter_by(id=a.student_id).first()

        data.append({
            "name": user.name if user else "",
            "student_id": a.student_id,
            "date": str(a.date),
            "time": str(a.time),
            "status": a.status,
            "latitude": a.latitude,
            "longitude": a.longitude,
            "address": a.address,
            "date_time": a.date_time
        })

    return jsonify({
        "success": True,
        "role": role,
        "data": data
    })