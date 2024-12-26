from flask import Flask
from config import Config
from app.routes.auth import init_firebase
from app.utils import load_site_info

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_firebase(app)

    # Import blueprints at function level to avoid circular imports
    from app.routes import auth, main  # pylint: disable=import-outside-toplevel
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)

    # Make site info available to all templates
    @app.context_processor
    def inject_site_info():
        return {'site_info': load_site_info()}

    return app
