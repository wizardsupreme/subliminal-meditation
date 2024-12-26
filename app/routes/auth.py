from flask import Blueprint, redirect, url_for, session, request, render_template, current_app
import firebase_admin
from firebase_admin import auth as firebase_auth
from firebase_admin import credentials
from functools import wraps
from datetime import datetime

bp = Blueprint('auth', __name__)

def init_firebase(app):
    if app.config.get('FIREBASE_ADMIN_CREDENTIALS'):
        cred = credentials.Certificate(app.config['FIREBASE_ADMIN_CREDENTIALS'])
    else:
        cred = credentials.Certificate(app.config['FIREBASE_ADMIN_SDK_PATH'])
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