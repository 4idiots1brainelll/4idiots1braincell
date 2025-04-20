from App.database import db
from App.models.user import User


class ReportRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(50))     # 'Enrollment', 'Staff', etc.
    year = db.Column(db.Integer)
    campus = db.Column(db.String(100))
    department = db.Column(db.String(100))
    program_name = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(100))
    metric_name = db.Column(db.String(100))
    value = db.Column(db.Float)
    unit = db.Column(db.String(20))
    notes = db.Column(db.Text, nullable=True)

    # Who uploaded it?
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='report_records')



    def __init__(self, report_type, year, campus, department, program_name, category, metric_name, value, unit, notes, user_id):
        self.report_type = report_type
        self.year = year
        self.campus = campus
        self.department = department
        self.program_name = program_name
        self.category = category
        self.metric_name = metric_name
        self.value = value
        self.unit = unit
        self.notes = notes
        self.user_id = user_id
