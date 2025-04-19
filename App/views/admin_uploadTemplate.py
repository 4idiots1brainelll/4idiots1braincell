from flask import Blueprint, redirect, render_template, request, flash, current_app, url_for, send_file
from werkzeug.utils import secure_filename
from App.models import  User
from App.models.uploaded_file import UploadedFile
from App.database import db
from datetime import datetime
import os

from flask_jwt_extended import current_user, jwt_required, get_jwt_identity

admin_upload_template_views = Blueprint('admin_upload_template_views', __name__, template_folder='../templates')

@admin_upload_template_views.route('/admin_uploadTemplate')
@jwt_required()
def admin_upload_template():
    user = current_user
    return render_template('admin_uploadTemplate.html', user=user)