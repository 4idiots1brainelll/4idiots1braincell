import os
from flask import Flask
from flask_cors import CORS
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from App.database import init_db
from App.config import load_config
from App.views import views, setup_admin
from App.controllers import setup_jwt, add_auth_context

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static')
    load_config(app, overrides)
    CORS(app)
    
    # Configure uploads and database
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
    app.config['ALLOWED_EXTENSIONS'] = {'xlsx', 'xls'}
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Or your DB URI
    
    # Initialize database
    from App.database import init_db
    init_db(app)
    
    # Rest of your initialization code
    add_auth_context(app)
    setup_jwt(app)
    setup_admin(app)
    
    # Register blueprints
    for view in views:
        app.register_blueprint(view)
    
    return app