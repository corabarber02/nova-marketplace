from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Listing

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile')
@login_required
def profile():
    listings = Listing.query.filter_by(user_id=current_user.id).order_by(Listing.created_at.desc()).all()
    return render_template('profile.html', listings=listings)