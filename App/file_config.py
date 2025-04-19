import os
from flask_uploads import UploadSet, DOCUMENTS

# File upload configurations
class FileConfig:
    UPLOAD_FOLDER = os.path.abspath('uploads')
    ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_SET = UploadSet('files', DOCUMENTS)  # Using only documents for Excel files

    @classmethod
    def init_app(cls, app):
        # Ensure upload folder exists
        os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)
        
        # Configure upload settings
        app.config['UPLOAD_FOLDER'] = cls.UPLOAD_FOLDER
        app.config['ALLOWED_EXTENSIONS'] = cls.ALLOWED_EXTENSIONS
        app.config['MAX_CONTENT_LENGTH'] = cls.MAX_CONTENT_LENGTH
        app.config['UPLOADED_FILES_DEST'] = cls.UPLOAD_FOLDER
        app.config['UPLOADED_FILES_ALLOW'] = cls.ALLOWED_EXTENSIONS



        