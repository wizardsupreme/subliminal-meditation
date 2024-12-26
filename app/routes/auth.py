from datetime import datetime
from functools import wraps
import os

from flask import (
    Blueprint, redirect, url_for, session,
    request, render_template
)
import firebase_admin
from firebase_admin import auth as firebase_auth
from firebase_admin import credentials

bp = Blueprint('auth', __name__)

def init_firebase(app):
    private_key = os.getenv('FIREBASE_PRIVATE_KEY')
    if not private_key:
        raise ValueError("FIREBASE_PRIVATE_KEY environment variable is not set")

    if app.config.get('FIREBASE_ADMIN_CREDENTIALS'):
        cred = credentials.Certificate(app.config['FIREBASE_ADMIN_CREDENTIALS'])
    else:
        # Construct credentials from environment variables
        cred_dict = {
            "type": "service_account",
            "project_id": app.config['FIREBASE_CONFIG']['projectId'],
            "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
            "private_key": private_key.replace('\\n', '\n'),
            "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
            "client_id": os.getenv('FIREBASE_CLIENT_ID'),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_CERT_URL')
        }
        cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/login')
def login():
    return render_template('login.html')

@bp.route('/auth/callback')
def auth_callback():
    # Handle Firebase authentication callback
    id_token = request.args.get('id_token')
    if not id_token:
        print("No ID token received")
        return redirect(url_for('main.index'))

    try:
        # Verify the ID token
        decoded_token = firebase_auth.verify_id_token(id_token)
        user_id = decoded_token['uid']

        # Get additional user info from Firebase
        user = firebase_auth.get_user(user_id)
        # Debug the user info more thoroughly
        print("User info from Firebase:")
        print(f"- Display Name: {user.display_name}")
        print(f"- Email: {user.email}")
        print(f"- Photo URL: {user.photo_url}")

        # Store user info in session
        session['user_id'] = user_id
        session['user_name'] = user.display_name or 'User'
        session['user_email'] = user.email or ''
        # Set photo URL with fallback
        photo_url = user.photo_url if user.photo_url else url_for('static', filename='img/default-avatar.png')
        session['user_photo'] = photo_url
        print(f"Final photo URL stored in session: {session['user_photo']}")
        session['last_login'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"Successfully authenticated user: {user_id}")
        return redirect(url_for('main.dashboard'))
    except Exception as e:
        print(f"Auth error (detailed): {str(e)}")
        return redirect(url_for('main.index'))

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
