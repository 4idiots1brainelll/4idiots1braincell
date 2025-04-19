# App/models/template_file.py

from App.database import db

class TemplateFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey('admin.id'))  # admin who uploaded
    created_at = db.Column(db.DateTime, default=db.func.now())