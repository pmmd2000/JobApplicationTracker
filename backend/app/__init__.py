import os
from flask import Flask
from flask_cors import CORS
from .config import config
from .database import init_db
from .routes import api


def create_app():
    """Application factory for creating Flask app."""
    app = Flask(__name__)
    
    # Load configuration
    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[env])
    
    # Configure CORS
    CORS(app, origins=[app.config['CORS_ORIGIN']], supports_credentials=True)
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    app.register_blueprint(api)
    
    return app


# Create app instance for Gunicorn
app = create_app()
