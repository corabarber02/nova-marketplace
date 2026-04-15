import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user
from extensions import db
from models import Listing, CATEGORIES

listings_bp = Blueprint('listings', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@listings_bp.route('/')
def index():
    category = request.args.get('category')
    if category and category in CATEGORIES:
        listings = Listing.query.filter_by(category=category).order_by(Listing.created_at.desc()).all()
    else:
        listings = Listing.query.order_by(Listing.created_at.desc()).all()
    return render_template('index.html', listings=listings, categories=CATEGORIES, active_category=category)


@listings_bp.route('/listings/new', methods=['GET', 'POST'])
@login_required
def new_listing():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        price = request.form.get('price', '').strip()
        category = request.form.get('category', '').strip()
        contact_info = request.form.get('contact_info', '').strip()

        if not all([title, description, price, category, contact_info]):
            flash('Please fill in all required fields.', 'danger')
            return render_template('listing_new.html', categories=CATEGORIES)

        if category not in CATEGORIES:
            flash('Invalid category selected.', 'danger')
            return render_template('listing_new.html', categories=CATEGORIES)

        try:
            price = float(price)
            if price < 0:
                raise ValueError
        except ValueError:
            flash('Please enter a valid price.', 'danger')
            return render_template('listing_new.html', categories=CATEGORIES)

        photo_filename = None
        file = request.files.get('photo')
        if file and file.filename:
            if allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()
                photo_filename = f"{uuid.uuid4().hex}.{ext}"
                upload_folder = current_app.config['UPLOAD_FOLDER']
                file.save(os.path.join(upload_folder, photo_filename))
            else:
                flash('Invalid image format. Allowed: png, jpg, jpeg, gif, webp.', 'danger')
                return render_template('listing_new.html', categories=CATEGORIES)

        listing = Listing(
            title=title,
            description=description,
            price=price,
            category=category,
            contact_info=contact_info,
            photo_filename=photo_filename,
            user_id=current_user.id
        )
        db.session.add(listing)
        db.session.commit()

        flash('Listing created successfully!', 'success')
        return redirect(url_for('listings.detail', listing_id=listing.id))

    return render_template('listing_new.html', categories=CATEGORIES)


@listings_bp.route('/listings/<int:listing_id>')
def detail(listing_id):
    listing = db.get_or_404(Listing, listing_id)
    return render_template('listing_detail.html', listing=listing)


@listings_bp.route('/listings/<int:listing_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_listing(listing_id):
    listing = db.get_or_404(Listing, listing_id)

    if listing.user_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        price = request.form.get('price', '').strip()
        category = request.form.get('category', '').strip()
        contact_info = request.form.get('contact_info', '').strip()

        if not all([title, description, price, category, contact_info]):
            flash('Please fill in all required fields.', 'danger')
            return render_template('listing_edit.html', listing=listing, categories=CATEGORIES)

        if category not in CATEGORIES:
            flash('Invalid category selected.', 'danger')
            return render_template('listing_edit.html', listing=listing, categories=CATEGORIES)

        try:
            price = float(price)
            if price < 0:
                raise ValueError
        except ValueError:
            flash('Please enter a valid price.', 'danger')
            return render_template('listing_edit.html', listing=listing, categories=CATEGORIES)

        file = request.files.get('photo')
        if file and file.filename:
            if allowed_file(file.filename):
                if listing.photo_filename:
                    old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], listing.photo_filename)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                ext = file.filename.rsplit('.', 1)[1].lower()
                new_filename = f"{uuid.uuid4().hex}.{ext}"
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename))
                listing.photo_filename = new_filename
            else:
                flash('Invalid image format. Allowed: png, jpg, jpeg, gif, webp.', 'danger')
                return render_template('listing_edit.html', listing=listing, categories=CATEGORIES)

        listing.title = title
        listing.description = description
        listing.price = price
        listing.category = category
        listing.contact_info = contact_info
        db.session.commit()

        flash('Listing updated successfully!', 'success')
        return redirect(url_for('listings.detail', listing_id=listing.id))

    return render_template('listing_edit.html', listing=listing, categories=CATEGORIES)


@listings_bp.route('/listings/<int:listing_id>/delete', methods=['POST'])
@login_required
def delete_listing(listing_id):
    listing = db.get_or_404(Listing, listing_id)

    if listing.user_id != current_user.id:
        abort(403)

    if listing.photo_filename:
        photo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], listing.photo_filename)
        if os.path.exists(photo_path):
            os.remove(photo_path)

    db.session.delete(listing)
    db.session.commit()

    flash('Listing deleted.', 'success')
    return redirect(url_for('listings.index'))