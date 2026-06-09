from services.database import db

class Employee(db.Model):

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    phone = db.Column(db.String(20))

    password = db.Column(db.String(255))

    photo = db.Column(db.String(255))

    status = db.Column(db.String(20))

    aadhar_number = db.Column(db.String(20))

    guardian_name = db.Column(db.String(100))

    email = db.Column(db.String(100))

    address = db.Column(db.Text)

    dob = db.Column(db.Date)

    emergency_contact = db.Column(db.String(20))

    role = db.Column(db.String(20))
    face_embedding = db.Column(db.Text)