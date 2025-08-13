# Student Portal (Flask)

A minimal Student Academic Details system built with Flask.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export FLASK_APP=manage.py  # Windows: set FLASK_APP=manage.py
flask db init
flask db migrate -m "initial"
flask db upgrade

python seeds/seed_admin.py
flask run
```

Login:
- username: `admin`
- password: `Admin@123`

Generated on 2025-08-13.
