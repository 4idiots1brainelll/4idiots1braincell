from datetime import datetime
from App.database import db

class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(512), nullable=False)  # Stores file system path
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='uploads')

    def __init__(self, filename, filepath, user_id):
        self.filename = filename
        self.filepath = filepath
        self.user_id = user_id

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'filepath': self.filepath,
            'user_id': self.user_id,
            'upload_date': self.upload_date.isoformat()
        }