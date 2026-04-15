from datetime import datetime
from flask_login import UserMixin
from extensions import db, login_manager

# Agreed category list — do not change without telling all team members
CATEGORIES = ['Sport', 'Home & Utilities', 'Clothing', 'Books', 'Transportation', 'Other']


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
