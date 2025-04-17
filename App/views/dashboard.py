from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize

from App.models import User


dashboard_views = Blueprint('dashboard_views', __name__, template_folder='../templates')

@dashboard_views.route('/dashboard', methods=['GET'])
def dashboard_page():
    user = User.query.first()
    return render_template('dashboard.html', user=user)