from flask import Blueprint, redirect, render_template, request, flash, current_app, url_for, send_file
from werkzeug.utils import secure_filename
from App.models import  User
from App.models.uploaded_file import UploadedFile
from App.database import db
from datetime import datetime
import os

from App.models.template_file import TemplateFile

from flask_jwt_extended import current_user, jwt_required, get_jwt_identity

admin_upload_template_views = Blueprint('admin_upload_template_views', __name__, template_folder='../templates')

@admin_upload_template_views.route('/admin_uploadTemplate')
@jwt_required()
def admin_upload_template():
    user = current_user
    return render_template('admin_uploadTemplate.html', user=user)

@admin_upload_template_views.route('/upload_template', methods=['POST'])
@jwt_required()
def upload_template():
    user = User.query.first()  # Should check if user is admin
    
    file = request.files.get('file')
    if not file or file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('upload_sheet_views.upload_sheet'))

    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config['TEMPLATE_UPLOAD_FOLDER'], filename)
    os.makedirs(current_app.config['TEMPLATE_UPLOAD_FOLDER'], exist_ok=True)
    file.save(filepath)

    new_template = TemplateFile(
        filename=filename,
        filepath=filepath,
        created_by=user.id
    )
    db.session.add(new_template)
    db.session.commit()

    flash(f'Template "{filename}" uploaded successfully!', 'success')
    return redirect(url_for('admin_upload_template_views.admin_upload_template'))