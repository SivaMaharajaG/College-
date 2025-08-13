from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class AddMarkForm(FlaskForm):
    student_id = SelectField("Student", coerce=int, validators=[DataRequired()])
    subject_id = SelectField("Subject", coerce=int, validators=[DataRequired()])
    marks_obtained = FloatField("Marks Obtained", validators=[DataRequired(), NumberRange(min=0)])
    total_marks = FloatField("Total Marks", validators=[DataRequired(), NumberRange(min=1)])
    exam_type = SelectField("Exam Type", choices=[("midterm","Midterm"),("final","Final"),("lab","Lab")], validators=[DataRequired()])
    submit = SubmitField("Save")
