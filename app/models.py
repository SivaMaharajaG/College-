from .extensions import db, bcrypt, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin/faculty/student
    twofa_secret = db.Column(db.String(16), nullable=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode()

    def check_password(self, pw):
        return bcrypt.check_password_hash(self.password_hash, pw)

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    dob = db.Column(db.Date)
    gender = db.Column(db.String(20))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    department = db.Column(db.String(120))
    admission_year = db.Column(db.Integer)
    photo = db.Column(db.String(300))

    marks = db.relationship("Mark", backref="student", lazy="dynamic")
    attendances = db.relationship("Attendance", backref="student", lazy="dynamic")

class Subject(db.Model):
    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(200))
    semester = db.Column(db.Integer)
    department = db.Column(db.String(120))

class Mark(db.Model):
    __tablename__ = "marks"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"))
    marks_obtained = db.Column(db.Float)
    total_marks = db.Column(db.Float)
    exam_type = db.Column(db.String(50))  # midterm/final/lab
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    subject = db.relationship("Subject")

class Attendance(db.Model):
    __tablename__ = "attendance"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"))
    date = db.Column(db.Date)
    status = db.Column(db.String(10))  # Present/Absent

    subject = db.relationship("Subject")

class Fee(db.Model):
    __tablename__ = "fees"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
    amount = db.Column(db.Float)
    status = db.Column(db.String(20))  # Paid/Unpaid
    due_date = db.Column(db.Date)

class AuditLog(db.Model):
    __tablename__ = "audit_log"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    action = db.Column(db.String(400))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
