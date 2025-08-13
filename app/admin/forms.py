from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FileField, SubmitField
from wtforms.validators import DataRequired, Optional

class AddStudentForm(FlaskForm):
    student_number = StringField("Student Number", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[Optional()])
    department = StringField("Department", validators=[Optional()])
    admission_year = IntegerField("Admission Year", validators=[Optional()])
    photo = FileField("Photo")
    submit = SubmitField("Add")
