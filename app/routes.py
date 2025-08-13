from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from ..models import Student

student_bp = Blueprint("student", __name__, template_folder="../templates/student")

@student_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.role != "student":
        return "Unauthorized", 403
    student = Student.query.filter_by(email=current_user.email).first()
    marks = []
    attendance = []
    if student:
        marks = [ {"subject":m.subject.name if m.subject else 'Unknown', "score":m.marks_obtained, "total":m.total_marks} for m in student.marks ]
        attendance = [ {"subject":a.subject.name if a.subject else 'Unknown', "date":a.date.isoformat() if a.date else '', "status":a.status} for a in student.attendances ]
    return render_template("student/dashboard.html", marks=marks, attendance=attendance)

@student_bp.route("/api/marks")
@login_required
def api_marks():
    student = Student.query.filter_by(email=current_user.email).first()
    rows = []
    if student:
        rows = [{"subject":m.subject.name if m.subject else 'Unknown', "percent": (m.marks_obtained/m.total_marks)*100 if (m.total_marks or 0) else 0} for m in student.marks]
    return jsonify(rows)
