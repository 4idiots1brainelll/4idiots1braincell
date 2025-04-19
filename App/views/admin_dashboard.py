from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize

from App.models import User
from flask_jwt_extended import current_user, jwt_required, get_jwt_identity

admin_dashboard_views = Blueprint('admin_dashboard_views', __name__, template_folder='../templates')

@admin_dashboard_views.route('/admin_dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard_page():
    user = current_user
    if user.type == 'admin':
        return render_template('admin_dashboard.html', user=user)
    return redirect('/dashboard')