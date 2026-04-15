# Prompt for Person 1 — Foundation (app.py, models.py, extensions.py, GitHub setup)

Paste everything below this line into a new Claude conversation.

---

I'm working on a web-based student marketplace called **Nova SBE Marketplace** using Python and Flask. I am Person 1 — I own the foundation of the project. The scaffold has already been created. My job is to understand all the existing files, maintain them, and be the person who helps integrate everyone's code.

## Project structure

```
nova-marketplace/
├── app.py
├── extensions.py
├── models.py
├── mock_students.json
├── requirements.txt
├── auth.py              ← Person 2 is building this
├── listings.py          ← Person 3 is building this
├── profile.py           ← Person 4 is building this
├── templates/
│   ├── base.html
│   └── index.html
└── static/
    ├── css/style.css
    └── uploads/
```

## Existing files (I own these — do not let teammates modify them)

### `extensions.py`
```python
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
```

### `app.py`
```python
import os
from flask import Flask
from extensions import db, login_manager


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'nova-sbe-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketplace.db'
    app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'

    from auth import auth_bp
    from listings import listings_bp
    from profile import profile_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(listings_bp)
    app.register_blueprint(profile_bp)

    with app.app_context():
        db.create_all()
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
```

### `models.py`
```python
from datetime import datetime
from flask_login import UserMixin
from extensions import db, login_manager

CATEGORIES = ['Books', 'Clothes', 'Furniture', 'Electronics', 'Other']


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    listings = db.relationship('Listing', backref='seller', lazy=True)


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    contact_info = db.Column(db.String(150), nullable=False)
    photo_filename = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
```

### `mock_students.json`
```json
{
  "student_ids": [
    "10001", "10002", "10003", "10004", "10005",
    "10006", "10007", "10008", "10009", "10010",
    "20001", "20002", "20003", "20004", "20005",
    "30001", "30002", "30003", "30004", "30005",
    "40001", "40002", "40003", "40004", "40005"
  ]
}
```

### `requirements.txt`
```
Flask==3.0.3
Flask-Login==0.6.3
Flask-SQLAlchemy==3.1.1
Werkzeug==3.0.3
```

---

## My responsibilities

### 1. Set up and run the project
Install dependencies and verify the app runs:
```bash
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows
pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5000` — the homepage should load with no errors.

### 2. Set up GitHub (do this first so teammates can clone the repo)
```bash
git init
git add .
git commit -m "initial scaffold"
```
Then on github.com: create a new repository called `nova-marketplace`, copy the two commands it gives you (`git remote add origin ...` and `git push`), and run them in the terminal.
Share the repo link with all teammates.

### 3. Understand the codebase
I need to be able to explain to my teammates:
- What `db` and `login_manager` are and why they live in `extensions.py`
- What the `User` and `Listing` models look like (fields, types, relationships)
- What `CATEGORIES` is and why teammates must not change it without asking
- How `create_app()` works and why blueprints are imported inside it

### 4. Help integrate teammates' code
When a teammate finishes their part and pushes to GitHub, I pull it and test that the full app still runs:
```bash
git pull
python app.py
```
If something breaks, I help diagnose it.

### 5. Add a `.gitignore` file
Create a `.gitignore` so that the virtual environment, database file, and uploaded photos are not pushed to GitHub:
```
venv/
instance/
*.db
static/uploads/*
__pycache__/
*.pyc
.DS_Store
```

---

Please help me:
1. Confirm I understand all the existing files correctly
2. Create the `.gitignore` file
3. Answer any questions I have about the code
4. Help me test that the app runs correctly end-to-end once teammates push their code
