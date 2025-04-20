from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, flash, url_for
from App.controllers import create_user, initialize

from App.models import User
from App.models.uploaded_file import *
from App.models.reportRecord import *

import os

from flask_jwt_extended import current_user, jwt_required, get_jwt_identity




viewreport_views = Blueprint('viewreport_views', __name__, template_folder='../templates')

@viewreport_views.route('/viewreport', methods=['GET'])
@jwt_required()
def viewreport_page():
    user = current_user

    uploaded_files = UploadedFile.query.filter_by(user_id=user.id).all()


    return render_template('viewreport.html', user=user, uploaded_files=uploaded_files)



@viewreport_views.route('/download/<int:file_id>', methods=['GET'])
@jwt_required()
def download_file(file_id):
    file = UploadedFile.query.get_or_404(file_id)

    # Check if user owns the file
    if file.user_id != current_user.id:
        flash("Unauthorized", "error")
        return redirect(url_for('viewreport_views.viewreport_page'))

    if os.path.exists(file.filepath):
        return send_from_directory(
            directory=os.path.dirname(file.filepath),
            path=os.path.basename(file.filepath),
            as_attachment=True
        )
    else:
        flash("File not found", "error")
        return redirect(url_for('viewreport_views.viewreport_page'))



@viewreport_views.route('/delete/<int:file_id>', methods=['POST'])
@jwt_required()
def delete_file(file_id):
    file = UploadedFile.query.get_or_404(file_id)
    
    # Delete associated ReportRecords
    ReportRecord.query.filter_by(user_id=file.user_id).delete()
    
    # Delete the file from disk
    if os.path.exists(file.filepath):
        os.remove(file.filepath)

    # Delete file record
    db.session.delete(file)
    db.session.commit()

    flash("Report and records deleted successfully", "success")
    return redirect(url_for('viewreport_views.viewreport_page'))