from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import jsonify

from datetime import datetime

import os
import json

from models.attendance import Attendance
from models.employee import Employee

from services.database import db
from services.face_service import FaceService

attendance_bp = Blueprint(
    "attendance",
    __name__
)


@attendance_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/")

    employee = Employee.query.get(
        session["user_id"]
    )

    total_attendance = Attendance.query.count()

    return render_template(
        "dashboard.html",
        user=employee,
        role=employee.role,
        total=total_attendance
    )


@attendance_bp.route("/attendance")
def attendance():

    if "user_id" not in session:
        return redirect("/")

    records = Attendance.query.filter_by(
        student_id=session["user_id"]
    ).order_by(
        Attendance.id.desc()
    ).all()

    return render_template(
        "attendance.html",
        records=records
    )


@attendance_bp.route("/mark-attendance")
def mark_attendance():

    if "user_id" not in session:
        return redirect("/")

    employee = Employee.query.get(
        session["user_id"]
    )

    return render_template(
        "mark_attendance.html",
        employee=employee
    )


@attendance_bp.route(
    "/verify-attendance",
    methods=["POST"]
)
@attendance_bp.route(
    "/verify-attendance",
    methods=["POST"]
)
def verify_attendance():

    if "user_id" not in session:
        return jsonify({
            "status": False,
            "message": "Please Login"
        })

    employee = Employee.query.get(
        session["user_id"]
    )

    if not employee:
        return jsonify({
            "status": False,
            "message": "Employee not found"
        })

    print("\n" + "=" * 60)
    print("LOGIN USER DETAILS")
    print("ID   :", employee.id)
    print("NAME :", employee.name)
    print("ROLE :", employee.role)
    print("=" * 60)

    image = request.files.get("image")

    latitude = request.form.get(
        "latitude",
        "0"
    )

    longitude = request.form.get(
        "longitude",
        "0"
    )
    address = request.form.get("address", "Unknown Location")

    if image is None:
        return jsonify({
            "status": False,
            "message": "Image Required"
        })

    upload_dir = "static/uploads"

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    image_path = os.path.join(
        upload_dir,
        f"{employee.id}_{int(datetime.now().timestamp())}.jpg"
    )

    image.save(image_path)

    try:

        if not employee.face_embedding:

            return jsonify({
                "status": False,
                "message": "No face embedding found"
            })

        face_service = FaceService()

        stored_embedding = json.loads(
            employee.face_embedding
        )

        stored_embedding = [
            float(x)
            for x in stored_embedding
        ]

        similarity = face_service.verify_face(
            image_path,
            stored_embedding
        )

        print()
        print("=" * 60)
        print("LOGIN USER")
        print("ID   :", employee.id)
        print("NAME :", employee.name)
        print("ROLE :", employee.role)
        print()
        print("SIMILARITY :", similarity)
        print("=" * 60)

        if similarity < 0.70:

            print("❌ FACE NOT MATCHED")

            return jsonify({
                "status": False,
                "similarity": round(similarity, 3),
                "message": "Face Not Matched"
            })

        print("✅ FACE MATCHED")

        last_attendance = Attendance.query.filter_by(
            student_id=employee.id
        ).order_by(
            Attendance.id.desc()
        ).first()

        attendance_status = "IN"

        if (
            last_attendance
            and last_attendance.status == "IN"
        ):
            attendance_status = "OUT"

        now = datetime.now()

        print("\n" + "=" * 60)
        print("ATTENDANCE MARKING")
        print("EMPLOYEE ID   :", employee.id)
        print("EMPLOYEE NAME :", employee.name)
        print("STATUS        :", attendance_status)
        print("LATITUDE      :", latitude)
        print("LONGITUDE     :", longitude)
        print("TIME          :", now)
        print("=" * 60)

        attendance = Attendance(
            student_id=employee.id,
            date=now.date(),
            time=now.time(),
            status=attendance_status,
            latitude=latitude,
            longitude=longitude,
            address=address,
            date_time=now.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        if attendance_status == "IN":
            attendance.in_time = now

        if attendance_status == "OUT":
            attendance.out_time = now

        db.session.add(attendance)
        db.session.commit()

        print("\n" + "=" * 60)
        print("ATTENDANCE SAVED SUCCESSFULLY")
        print("EMPLOYEE :", employee.name)
        print("STATUS   :", attendance_status)
        print("DATE     :", now.date())
        print("TIME     :", now.time())
        print("=" * 60)

        return jsonify({
            "status": True,
            "attendance": attendance_status,
            "similarity": round(similarity, 3),
            "message": f"Attendance {attendance_status} Marked Successfully"
        })

    except Exception as e:

        print("ERROR :", str(e))

        return jsonify({
            "status": False,
            "message": str(e)
        })