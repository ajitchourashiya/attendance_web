from flask import Flask
from config import Config
from services.database import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# ---------------------------
# BLUEPRINT IMPORTS
# ---------------------------
from routes.auth import auth_bp
from routes.employee import employee_bp
from routes.attendance import attendance_bp
from routes.role import role_bp
from routes.view_attendance import view_attendance_bp   # ✅ NEW ROUTE

# ---------------------------
# REGISTER BLUEPRINTS
# ---------------------------
app.register_blueprint(auth_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(role_bp)
app.register_blueprint(view_attendance_bp)  # ✅ NEW REGISTERED

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )