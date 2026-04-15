from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__)


# ----------------------------------------------------------------
# TODO (Person 2): Replace these stubs with real implementations.
# See PERSON2_PROMPT.md for full instructions.
# ----------------------------------------------------------------

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    return 'Register page — coming soon'


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return 'Login page — coming soon'


@auth_bp.route('/logout')
def logout():
    return 'Logout — coming soon'
