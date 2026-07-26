from flask import Flask
from flask_cors import CORS
import os

def create_app():
    """Application factory function to create Flask app"""
    app = Flask(__name__)
    CORS(app)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # Import and register blueprints
    from app.routes import inventory_bp
    app.register_blueprint(inventory_bp, url_prefix='/api')
    
    return app
