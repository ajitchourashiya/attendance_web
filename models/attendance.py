from services.database import db

class Attendance(db.Model):

    __tablename__ = "attendance"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer
    )

    date = db.Column(
        db.Date
    )

    time = db.Column(
        db.Time
    )

    status = db.Column(
        db.String(20)
    )

    latitude = db.Column(
        db.Float
    )

    longitude = db.Column(
        db.Float
    )

    address = db.Column(
        db.Text
    )

    date_time = db.Column(
        db.String(50)
    )

    in_time = db.Column(
        db.DateTime
    )

    out_time = db.Column(
        db.DateTime
    )