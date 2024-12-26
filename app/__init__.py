from flask import Flask
from config import Config
from app.routes.auth import init_firebase

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_firebase(app)

    # Import blueprints at function level to avoid circular imports
    from app.routes import auth, main  # pylint: disable=import-outside-toplevel
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)

    return app
