# Prompt for Person 4 — Profile Page

Paste everything below this line into a new Claude conversation.

---

I'm building a web-based student marketplace called **Nova SBE Marketplace** using Python and Flask. The scaffold is already set up by a teammate. My job is to implement the **user profile page** by filling in `profile.py` and creating `templates/profile.html`.

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

### `profile.py` — current stub (I need to replace this)
```python
from flask import Blueprint

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile')
def profile():
    return 'Profile page — coming soon'
```

### `templates/base.html` (already created — my template must extend this)
The base template uses Bootstrap 5 and already has a navbar with a "My Profile" link pointing to `url_for('profile.profile')`. Photos are served from `static/uploads/`. It handles flash messages automatically.

### Other routes already built by teammates (I can link to these)
- `url_for('listings.index')` — homepage / browse all listings
- `url_for('listings.detail', listing_id=X)` — view a single listing
- `url_for('listings.edit_listing', listing_id=X)` — edit a listing
- `url_for('listings.delete_listing', listing_id=X)` — delete a listing (POST only)
- `url_for('listings.new_listing')` — create a new listing

---

## What I need to build

### 1. `profile.py` — replace the stub with a real implementation

**`/profile` (GET)** — requires login (`@login_required`)
- Load the currently logged-in user (`current_user`)
- Load all of their listings ordered by newest first:
  `listings = Listing.query.filter_by(user_id=current_user.id).order_by(Listing.created_at.desc()).all()`
- Render `profile.html` passing `listings`

### 2. `templates/profile.html`

Must extend `base.html`.

The page should show:
- The user's name and email at the top
- A count of how many active listings they have
- A "Sell New Item" button linking to `listings.new_listing`
- A grid of the user's listings (same card style as the homepage):
  - Listing photo (or placeholder icon if none)
  - Title, category badge, price
  - Buttons: "View", "Edit", and "Delete"
  - The Delete button must use a `<form method="POST">` pointing to the delete route (not a link)
- If the user has no listings, show a friendly empty state message with a link to create one

---

## Style guide
- Use `@login_required` from `flask_login`
- Use Bootstrap 5 classes (CDN already in base.html — do not add it again)
- Cards should use the same style as the homepage: `card h-100 shadow-sm`, image height 200px, `object-fit: cover`
- Do not modify any other files

Please generate the complete final `profile.py` and `templates/profile.html`.
