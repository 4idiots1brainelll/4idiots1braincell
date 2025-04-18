from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize

from App.models import User


viewreport_views = Blueprint('viewreport_views', __name__, template_folder='../templates')

@viewreport_views.route('/viewreport', methods=['GET'])
def viewreport_page():
    user = User.query.first()
    return render_template('viewreport.html', user=user)