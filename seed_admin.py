from app import create_app
from app.extensions import db
from app.models import User, Subject

app = create_app()
with app.app_context():
    # Admin user
    if not User.query.filter_by(username='admin').first():
        u = User(username='admin', email='admin@example.com', role='admin')
        u.set_password('Admin@123')
        db.session.add(u)
        db.session.commit()
        print("Admin created: admin / Admin@123")

    # Sample faculty user
    if not User.query.filter_by(username='faculty1').first():
        u = User(username='faculty1', email='faculty1@example.com', role='faculty')
        u.set_password('Faculty@123')
        db.session.add(u)

    # Sample student user (for dashboard demo; match with a Student later)
    if not User.query.filter_by(username='student1').first():
        u = User(username='student1', email='student1@example.com', role='student')
        u.set_password('Student@123')
        db.session.add(u)

    # Seed a few subjects
    if Subject.query.count() == 0:
        db.session.add_all([
            Subject(code="CS101", name="Programming Fundamentals", semester=1, department="CSE"),
            Subject(code="MA101", name="Calculus I", semester=1, department="CSE"),
            Subject(code="PH101", name="Physics I", semester=1, department="CSE"),
        ])
        print("Seeded subjects")

    db.session.commit()
    print("Seeding complete.")
