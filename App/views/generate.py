from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize

from App.models import User
from flask_jwt_extended import current_user, jwt_required, get_jwt_identity


generate_views = Blueprint('generate_views', __name__, template_folder='../templates')

@generate_views.route('/generate', methods=['GET'])
@jwt_required()
def dashboard_page():
    user = current_user
    return render_template('generate.html', user=user)