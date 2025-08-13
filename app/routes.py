from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_file
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Student, Subject, Mark
import pandas as pd
import io, os, csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from werkzeug.utils import secure_filename
from .forms import AddStudentForm

admin_bp = Blueprint("admin", __name__, template_folder="../templates/admin")

def is_admin():
    return current_user.is_authenticated and current_user.role == "admin"

@admin_bp.route("/students/add", methods=["GET","POST"])
@login_required
def add_student():
    if not is_admin():
        flash("Unauthorized", "danger"); return redirect(url_for("index"))
    form = AddStudentForm()
    if form.validate_on_submit():
        s = Student(
            student_number=form.student_number.data,
            name=form.name.data,
            email=form.email.data,
            department=form.department.data,
            admission_year=form.admission_year.data or None
        )
        f = form.photo.data
        if f:
            filename = secure_filename(f.filename)
            path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            f.save(path)
            s.photo = filename
        db.session.add(s); db.session.commit()
        flash("Student added", "success")
        return redirect(url_for(".list_students"))
    return render_template("admin/add_student.html", form=form)

@admin_bp.route("/students")
@login_required
def list_students():
    if not is_admin(): flash("Unauthorized", "danger"); return redirect(url_for("index"))
    page = int(request.args.get("page", 1))
    students = Student.query.paginate(page=page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
    return render_template("admin/list_students.html", students=students)

@admin_bp.route("/students/import", methods=["POST"])
@login_required
def import_students():
    if not is_admin(): flash("Unauthorized", "danger"); return redirect(url_for(".list_students"))
    f = request.files.get("file")
    if not f: flash("No file", "danger"); return redirect(url_for(".list_students"))
    df = pd.read_csv(f)
    for _, row in df.iterrows():
        s = Student(
            student_number=row['student_number'],
            name=row['name'],
            email=row.get('email'),
            department=row.get('department'),
            admission_year=int(row.get('admission_year', 0)) if row.get('admission_year') else None
        )
        db.session.add(s)
    db.session.commit()
    flash("Imported", "success")
    return redirect(url_for(".list_students"))

@admin_bp.route("/marks/export")
@login_required
def export_marks():
    if not is_admin(): flash("Unauthorized", "danger"); return redirect(url_for("index"))
    marks = Mark.query.all()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['student', 'subject', 'marks_obtained', 'total', 'exam_type'])
    for m in marks:
        cw.writerow([m.student.name if m.student else '', m.subject.name if m.subject else '', m.marks_obtained, m.total_marks, m.exam_type])
    output = io.BytesIO()
    output.write(si.getvalue().encode())
    output.seek(0)
    return send_file(output, download_name="marks.csv", as_attachment=True)

@admin_bp.route("/students/<int:sid>/marksheet")
@login_required
def marksheet(sid):
    if not is_admin(): flash("Unauthorized", "danger"); return redirect(url_for("index"))
    student = Student.query.get_or_404(sid)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, f"Marksheet - {student.name} ({student.student_number})")
    y = 760
    c.setFont("Helvetica", 12)
    marks = student.marks.all()
    for m in marks:
        subj = m.subject.name if m.subject else 'Unknown'
        code = m.subject.code if m.subject else '---'
        c.drawString(60, y, f"{subj} ({code}): {m.marks_obtained}/{m.total_marks} [{m.exam_type}]")
        y -= 20
        if y < 50:
            c.showPage(); y = 800
    c.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"{student.student_number}_marks.pdf", mimetype='application/pdf')
