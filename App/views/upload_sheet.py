from flask import Blueprint, redirect, render_template, request, flash, current_app, url_for, send_file
from werkzeug.utils import secure_filename
from App.models import  User, ReportRecord
from App.models.uploaded_file import UploadedFile
from App.database import db
from datetime import datetime
import os
from flask_jwt_extended import current_user, jwt_required, get_jwt_identity
import pandas as pd

upload_sheet_views = Blueprint('upload_sheet_views', __name__, template_folder='../templates')

@upload_sheet_views.route('/upload_sheet')
@jwt_required()
def upload_sheet():
    user = current_user
    return render_template('upload_sheet.html', user=user)

@upload_sheet_views.route('/upload', methods=['POST'])
@jwt_required()
def handle_upload():
    user = current_user
    
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

            df = pd.read_excel(filepath)

            df.columns = [col.strip().lower().replace(" ", "").replace("_", "") for col in df.columns]

            col_map = {
                'report_type': 'reporttype',
                'year': 'year',
                'campus': 'campus',
                'department': 'department',
                'program_name': 'programname',
                'category': 'category',
                'metric_name': 'metricname',
                'value': 'value',
                'unit': 'unit',
                'notes': 'notes'
            }

            required_columns = list(col_map.values())

            # Validate
            if not all(col in df.columns for col in required_columns):
                raise Exception("Excel file missing required columns.")

            # Loop and insert
            for _, row in df.iterrows():
                record = ReportRecord(
                    report_type=row[col_map['report_type']],
                    year=int(row[col_map['year']]),
                    campus=row[col_map['campus']],
                    department=row[col_map['department']],
                    program_name=row.get(col_map['program_name']),
                    category=row[col_map['category']],
                    metric_name=row[col_map['metric_name']],
                    value=float(row[col_map['value']]),
                    unit=row[col_map['unit']],
                    notes=row.get(col_map['notes']),
                    user_id=user.id
                )
                db.session.add(record)

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


@upload_sheet_views.route('/download/<int:file_id>')
@jwt_required()
def download_file(file_id):
    user = current_user
    
    uploaded_file = UploadedFile.query.get_or_404(file_id)

    if uploaded_file.user_id != user.id:
        flash('You do not have permission to download this file.', 'error')


    return send_file(uploaded_file.filepath, as_attachment=True)