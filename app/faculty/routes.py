from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Student, Subject, Mark
from .forms import AddMarkForm

faculty_bp = Blueprint("faculty", __name__, template_folder="../templates/faculty")

def is_faculty():
    return current_user.is_authenticated and current_user.role == "faculty"

@faculty_bp.route("/marks/add", methods=["GET","POST"])
@login_required
def add_mark():
    if not is_faculty(): flash("Unauthorized", "danger"); return redirect(url_for("index"))
    form = AddMarkForm()
    form.student_id.choices = [(s.id, f"{s.name} ({s.student_number})") for s in Student.query.order_by(Student.name).all()]
    form.subject_id.choices = [(s.id, f"{s.name} ({s.code})") for s in Subject.query.order_by(Subject.name).all()]
    if form.validate_on_submit():
        m = Mark(
            student_id=form.student_id.data,
            subject_id=form.subject_id.data,
            marks_obtained=form.marks_obtained.data,
            total_marks=form.total_marks.data,
            exam_type=form.exam_type.data
        )
        db.session.add(m); db.session.commit()
        flash("Marks added", "success")
        return redirect(url_for(".add_mark"))
    return render_template("faculty/add_mark.html", form=form)
