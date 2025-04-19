from flask import Blueprint, redirect, render_template, request, flash, current_app, url_for, send_file
from werkzeug.utils import secure_filename
from App.models import  User
from App.models.uploaded_file import UploadedFile
from App.database import db
from datetime import datetime
import os


upload_sheet_views = Blueprint('upload_sheet_views', __name__, template_folder='../templates')

@upload_sheet_views.route('/upload_sheet')
def upload_sheet():
    user = User.query.first()
    return render_template('upload_sheet.html', user=user)

@upload_sheet_views.route('/upload', methods=['POST'])
def handle_upload():
    user = User.query.first()
    
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('upload_sheet_views.upload_sheet'))

    file = request.files['file']

    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('upload_sheet_views.upload_sheet'))

    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_filename = f"{timestamp}_{filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)

            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(filepath)

            uploaded_file = UploadedFile(
                filename=filename,
                filepath=filepath,
                user_id=user.id
            )
            db.session.add(uploaded_file)
            db.session.commit()

            flash(f'File "{filename}" uploaded successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error uploading file: {str(e)}', 'error')
    else:
        flash('Only .xlsx and .xls files are allowed', 'error')

    return redirect(url_for('upload_sheet_views.upload_sheet'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']