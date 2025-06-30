from flask import Blueprint, render_template
from src.utils.auth_decorators import login_required

user_panel_bp = Blueprint('user_panel', __name__)

@user_panel_bp.route('/user_panel/dashboard')
@login_required('user')
def user_dashboard():
    return render_template('user_panel/user_dashboard.html', head_title="Panel Usuario")