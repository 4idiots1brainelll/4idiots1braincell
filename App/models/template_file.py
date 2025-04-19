# App/models/template_file.py

from App.database import db

from App.models.user import User
from App.models.admin import Admin

class TemplateFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))  # admin who uploaded
    created_at = db.Column(db.DateTime, default=db.func.now())


    def __init__(self, filename, filepath, created_by):
        self.filename = filename
        self.filepath = filepath
        self.created_by = created_by

