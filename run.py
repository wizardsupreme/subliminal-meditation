import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Enable debug mode only in development
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode)
