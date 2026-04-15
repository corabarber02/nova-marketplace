from flask import Blueprint

profile_bp = Blueprint('profile', __name__)


# ----------------------------------------------------------------
# TODO (Person 4): Replace this stub with a real implementation.
# See PERSON4_PROMPT.md for full instructions.
# ----------------------------------------------------------------

@profile_bp.route('/profile')
def profile():
    return 'Profile page — coming soon'
