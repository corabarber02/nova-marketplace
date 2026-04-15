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


# ----------------------------------------------------------------
# TODO (Person 3): Replace these stubs with real implementations.
# See PERSON3_PROMPT.md for full instructions.
# ----------------------------------------------------------------

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
