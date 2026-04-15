# Prompt for Person 3 — Listings (Create, Edit, Delete, View)

Paste everything below this line into a new Claude conversation.

---

I'm building a web-based student marketplace called **Nova SBE Marketplace** using Python and Flask. The scaffold is already set up by a teammate. My job is to implement **listing creation, editing, deletion, and detail view** by filling in `listings.py` and creating the HTML templates.

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

### `listings.py` — current stub (I need to replace the stub routes below the index route)
```python
from flask import Blueprint, render_template, request
from models import Listing, CATEGORIES

listings_bp = Blueprint('listings', __name__)

@listings_bp.route('/')
def index():
    category = request.args.get('category')
    if category and category in CATEGORIES:
        listings = Listing.query.filter_by(category=category).order_by(Listing.created_at.desc()).all()
    else:
        listings = Listing.query.order_by(Listing.created_at.desc()).all()
    return render_template('index.html', listings=listings, categories=CATEGORIES, active_category=category)

@listings_bp.route('/listings/new', methods=['GET', 'POST'])
def new_listing():
    return 'New listing — coming soon'

@listings_bp.route('/listings/<int:listing_id>')
def detail(listing_id):
    return 'Listing detail — coming soon'

@listings_bp.route('/listings/<int:listing_id>/edit', methods=['GET', 'POST'])
def edit_listing(listing_id):
    return 'Edit listing — coming soon'

@listings_bp.route('/listings/<int:listing_id>/delete', methods=['POST'])
def delete_listing(listing_id):
    return 'Delete listing — coming soon'
```

### `templates/base.html` (already created — all my templates must extend this)
The base template uses Bootstrap 5. Photos are served from `static/uploads/`.

---

## What I need to build

### 1. `listings.py` — replace stub routes with real implementations

Keep the `index` route exactly as-is. Only replace the four stub routes below it.

**`/listings/new` (GET + POST)** — requires login (`@login_required`)
- GET: show a form to create a new listing
- POST:
  1. Read title, description, price, category, contact_info from the form
  2. If a photo was uploaded: save it to `static/uploads/` with a unique filename (use `uuid` to avoid name collisions). Only allow image files (png, jpg, jpeg, gif, webp).
  3. Save a new `Listing` to the database, set `user_id = current_user.id`
  4. Flash a success message, redirect to the listing's detail page

**`/listings/<int:listing_id>` (GET)** — public
- Fetch the listing by ID (use `db.get_or_404`)
- Render a detail page showing all fields

**`/listings/<int:listing_id>/edit` (GET + POST)** — requires login
- Only the listing's owner (`listing.user_id == current_user.id`) may edit it; otherwise abort(403)
- GET: show a pre-filled edit form
- POST: update the listing fields; if a new photo is uploaded replace the old one

**`/listings/<int:listing_id>/delete` (POST)** — requires login
- Only the owner may delete; otherwise abort(403)
- Delete the listing from the database, also delete the photo file from disk if it exists
- Redirect to the homepage

### 2. Templates to create

**`templates/listing_new.html`**
Form fields: Title, Description, Price (number), Category (dropdown from CATEGORIES), Contact Info, Photo (optional file input).
Must extend `base.html`. Use Bootstrap form classes.

**`templates/listing_detail.html`**
Show all listing fields. Show the photo if present. Show seller's name.
If the current user is the owner, show Edit and Delete buttons.
The Delete button must use a `<form method="POST">` (not a link) to hit the delete route.
Must extend `base.html`.

**`templates/listing_edit.html`**
Same fields as listing_new.html but pre-filled with the listing's current values.
Must extend `base.html`.

---

## Style guide
- Use `@login_required` from `flask_login` on routes that require a logged-in user
- Use `flask.flash` for success/error messages
- Use Bootstrap 5 classes (CDN already loaded in base.html)
- Do not modify `index`, `models.py`, `app.py`, or any other teammate's files

Please generate the complete final `listings.py` and all three templates.
