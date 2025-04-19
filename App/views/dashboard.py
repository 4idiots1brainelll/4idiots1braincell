from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize

from App.models import User
from flask_jwt_extended import current_user, jwt_required, get_jwt_identity


dashboard_views = Blueprint('dashboard_views', __name__, template_folder='../templates')

@dashboard_views.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard_page():
    user = current_user
    if user.type == 'admin':
        return render_template('admin_dashboard.html', user=user)
    return render_template('dashboard.html', user=user)