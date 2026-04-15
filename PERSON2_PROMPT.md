# Prompt for Person 2 — Auth (Register + Login + Logout)

Paste everything below this line into a new Claude conversation.

---

I'm building a web-based student marketplace called **Nova SBE Marketplace** using Python and Flask. The scaffold is already set up by a teammate. My job is to implement **user registration, login, and logout** by filling in `auth.py` and creating the HTML templates for register and login.

## What already exists (do not change these)

### `app.py`
```python
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

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
from app import db, login_manager

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

### `templates/base.html` (already created — all my templates must extend this)
The base template uses Bootstrap 5 and already has a navbar with links to:
- `url_for('auth.login')` — login page
- `url_for('auth.register')` — register page
- `url_for('auth.logout')` — logout
- `url_for('profile.profile')` — profile page
- `url_for('listings.new_listing')` — new listing page

It shows `current_user.is_authenticated` in the navbar to switch between logged-in and logged-out states.

---

## What I need to build

### 1. `auth.py` — replace the stubs with real implementations

The blueprint is named `auth_bp` and must stay registered as `auth`.

Implement these three routes:

**`/register` (GET + POST)**
- GET: show a registration form
- POST: validate the form, then:
  1. Check the student ID exists in `mock_students.json`
  2. Check the email is not already registered
  3. Check the student ID is not already registered
  4. Hash the password with `werkzeug.security.generate_password_hash`
  5. Save a new `User` to the database
  6. Log the user in with `flask_login.login_user`
  7. Redirect to the homepage (`listings.index`)
  8. On any error, flash an error message and re-show the form

**`/login` (GET + POST)**
- GET: show a login form
- POST:
  1. Look up the user by email
  2. Check the password with `werkzeug.security.check_password_hash`
  3. Log the user in and redirect to the homepage
  4. On failure, flash an error and re-show the form

**`/logout`**
- Call `flask_login.logout_user` and redirect to the homepage

### 2. `templates/register.html`
A form with fields: Full Name, Email, Password, Student ID.
Must extend `base.html`.
Use Bootstrap form classes. Show a link to the login page at the bottom.

### 3. `templates/login.html`
A form with fields: Email, Password.
Must extend `base.html`.
Use Bootstrap form classes. Show a link to the register page at the bottom.

---

## Style guide
- Use `flask.flash` for all user-facing error and success messages
- Keep it simple — no JavaScript validation, just server-side
- Use Bootstrap 5 classes for layout (the CDN is already loaded in base.html)
- Do not modify any files other than `auth.py`, `templates/register.html`, and `templates/login.html`

Please generate the complete contents of all three files.
