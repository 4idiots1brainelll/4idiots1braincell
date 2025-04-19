from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize

from App.models import User


download_views = Blueprint('download_views', __name__, template_folder='../templates')


@download_views.route('/download', methods=['GET'])
def download_template():
    user = User.query.first()
    return render_template("download.html" , user=user)