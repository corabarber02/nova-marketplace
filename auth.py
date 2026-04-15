import json
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from models import User

auth_bp = Blueprint('auth', __name__)

def load_valid_student_ids():
    with open('mock_students.json') as f:
        data = json.load(f)
    return data['student_ids']

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name       = request.form.get('name', '').strip()
        email      = request.form.get('email', '').strip()
        password   = request.form.get('password', '')
        student_id = request.form.get('student_id', '').strip()

        valid_ids = load_valid_student_ids()
        if student_id not in valid_ids:
            flash('Student ID not recognised.', 'danger')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Email is already registered.', 'danger')
            return render_template('register.html')

        if User.query.filter_by(student_id=student_id).first():
            flash('Student ID is already registered.', 'danger')
            return render_template('register.html')

        hashed_pw = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_pw, student_id=student_id)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash('Account created! Welcome to Nova SBE Marketplace.', 'success')
        return redirect(url_for('listings.index'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid email or password.', 'danger')
            return render_template('login.html')

        login_user(user)
        return redirect(url_for('listings.index'))

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('listings.index'))