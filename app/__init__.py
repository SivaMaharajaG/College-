from flask import Flask
from .config import Config
from .extensions import db, migrate, login_manager, bcrypt, mail
import os

def create_app(config_class=Config):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_class)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    login_manager.login_view = "auth.login"

    from .auth.routes import auth_bp
    from .admin.routes import admin_bp
    from .faculty.routes import faculty_bp
    from .student.routes import student_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(faculty_bp, url_prefix="/faculty")
    app.register_blueprint(student_bp, url_prefix="/student")

    @app.route("/")
    def index():
        return "Student Academic Details Portal — visit /auth/login"

    return app
