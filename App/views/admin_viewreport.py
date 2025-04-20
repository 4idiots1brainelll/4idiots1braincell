from flask import Blueprint, redirect, render_template, request, send_from_directory, flash, url_for
from App.models.uploaded_file import *
from App.models.reportRecord import *
from App.database import db 
import os
from flask_jwt_extended import current_user, jwt_required

admin_viewreport_views = Blueprint('admin_viewreport_views', __name__, template_folder='../templates')

@admin_viewreport_views.route('/admin_viewreport', methods=['GET'])
@jwt_required()
def admin_viewreport_page():
    # Ensure the current user is an admin
    if not hasattr(current_user, 'type') or current_user.type != 'admin':
        flash("Access denied: Admins only", "error")
        return redirect(url_for('dashboard_views.dashboard_page'))

    # Fetch all uploaded files
    uploaded_files = UploadedFile.query.all()

    return render_template('admin_viewreport.html', user=current_user, uploaded_files=uploaded_files)


@admin_viewreport_views.route('/admin_viewreport/download/<int:file_id>', methods=['GET'])
@jwt_required()
def admin_download_file(file_id):
    # Ensure the current user is an admin
    if not hasattr(current_user, 'type') or current_user.type != 'admin':
        flash("Access denied: Admins only", "error")
        return redirect(url_for('admin_viewreport_views.admin_viewreport_page'))

    file = UploadedFile.query.get_or_404(file_id)

    if os.path.exists(file.filepath):
        return send_from_directory(
            directory=os.path.dirname(file.filepath),
            path=os.path.basename(file.filepath),
            as_attachment=True
        )
    else:
        flash("File not found", "error")
        return redirect(url_for('admin_viewreport_views.admin_viewreport_page'))


@admin_viewreport_views.route('/admin_viewreport/delete/<int:file_id>', methods=['POST'])
@jwt_required()
def admin_delete_file(file_id):
    # Ensure the current user is an admin
    if not hasattr(current_user, 'type') or current_user.type != 'admin':
        flash("Access denied: Admins only", "error")
        return redirect(url_for('admin_viewreport_views.admin_viewreport_page'))

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
    return redirect(url_for('admin_viewreport_views.admin_viewreport_page'))