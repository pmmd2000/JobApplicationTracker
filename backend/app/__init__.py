import os
from flask import Flask
from flask_cors import CORS
from .config import config
from .database import init_db
from .routes import api


def create_app():
    """Application factory for creating Flask app."""
    app = Flask(__name__)
    
    # Trust reverse proxy headers
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    # Load configuration
    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[env])
    
    # Configure CORS
    CORS(app, origins=[app.config['CORS_ORIGIN']], supports_credentials=True)
    
    # Initialize compression
    from flask_compress import Compress
    Compress(app)
    
    # Initialize database and oauth
    init_db(app)
    from .extensions import oauth
    oauth.init_app(app)
    
    # Register blueprints
    app.register_blueprint(api)
    from .auth import auth
    app.register_blueprint(auth)
    
    return app


# Create app instance for Gunicorn
app = create_app()
