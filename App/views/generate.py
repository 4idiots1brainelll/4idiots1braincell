from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize

from App.models import User, ReportRecord
from flask_jwt_extended import current_user, jwt_required, get_jwt_identity


generate_views = Blueprint('generate_views', __name__, template_folder='../templates')

@generate_views.route('/generate', methods=['GET'])
@jwt_required()
def dashboard_page():
    user = current_user
    rec = ReportRecord.query.all()
    records = ReportRecord.query.filter_by(user_id=user.id).all()
    unique_years = sorted({r.year for r in rec}) 

    camp = ReportRecord.query.filter_by(user_id=user.id).all()
    unique_campuses = sorted({r.campus for r in camp})

    enroll = ReportRecord.query.filter_by(user_id=user.id).all()
    unique_reports = sorted({r.report_type for r in enroll})

    return render_template('generate.html', user=user, records=records, unique_years=unique_years, unique_campuses=unique_campuses, unique_reports=unique_reports)


@generate_views.route('/generate_chart_data', methods=['POST'])
def generate_chart_data():
    user = current_user
    year = request.form.get('year')
    campus = request.form.get('campus')
    report_type = request.form.get('report')
    chart_type = request.form.get('chartType')

    records = ReportRecord.query.filter_by( 
        year=year,
        campus=campus,
        report_type=report_type,
    ).all()

    # Simulate data (You can replace this with actual data processing)
    if report_type == 'Enrollment':
        fullSum = sum(record.value for record in records if record.metric_name == 'Full-Time Enrollment')
        partSum = sum(record.value for record in records if record.metric_name == 'Part-Time Enrollment')
        data = [
            {"label": "Full-Time", "value": fullSum},
            {"label": "Part-Time", "value": partSum}
        ]
    elif report_type == 'Staff':
        fullSSum = sum(record.value for record in records if record.metric_name == 'Full-Time Staff')
        partSSum = sum(record.value for record in records if record.metric_name == 'Part-Time Staff')
        data = [
            {"label": "Full-Time Staff", "value": fullSSum},
            {"label": "Part-Time Staff", "value": partSSum}
        ]

    
    # if year == '2024':
    #     data = [
    #         {"label": "Category 1", "value": 10},
    #         {"label": "Category 2", "value": 20},
    #     ]
    # elif year == '2023':
    #     data = [
    #         {"label": "cry", "value": 15},
    #         {"label": "hard", "value": 25},
    #         {"label": "hard", "value": 25}
    #     ]

    return jsonify({'chartType': chart_type, 'data': data})