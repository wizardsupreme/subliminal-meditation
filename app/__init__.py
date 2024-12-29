"""Flask application factory module."""
import os
from flask import Flask
from flask_session import Session
from config import Config
from app.routes.auth import init_firebase
from app.routes import auth, main
from app.utils import load_site_info
 # pylint: disable=import-outside-toplevel
def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    # Initialize Flask-Session
    Session(app)
    # Load site info and add to config
    site_info = load_site_info()
    app.config['SITE_NAME'] = site_info['site']['name']
    # Use Firebase config from Config class
    app.config['FIREBASE_API_KEY'] = app.config['FIREBASE_CONFIG']['apiKey']
    app.config['FIREBASE_AUTH_DOMAIN'] = app.config['FIREBASE_CONFIG']['authDomain']
    app.config['FIREBASE_PROJECT_ID'] = app.config['FIREBASE_CONFIG']['projectId']
    app.config['FIREBASE_STORAGE_BUCKET'] = app.config['FIREBASE_CONFIG']['storageBucket']
    app.config['FIREBASE_MESSAGING_SENDER_ID'] = app.config['FIREBASE_CONFIG']['messagingSenderId']
    app.config['FIREBASE_APP_ID'] = app.config['FIREBASE_CONFIG']['appId']
    init_firebase(app)
    # Import blueprints at function level to avoid circular imports
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    # Make site info available to all templates
    @app.context_processor
    def inject_site_info():
        """Make site info available to all templates."""
        return {'site_info': site_info}
    return app
