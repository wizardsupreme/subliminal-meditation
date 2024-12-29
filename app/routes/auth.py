"""Authentication routes and utilities."""
from datetime import datetime
from functools import wraps
import os

import firebase_admin
from firebase_admin import credentials
import jwt
from flask import (
    Blueprint, redirect, url_for, session,
    request, render_template
)

bp = Blueprint("auth", __name__)

def init_firebase(app):
    """Initialize Firebase Admin SDK."""
    private_key = os.getenv("FIREBASE_PRIVATE_KEY")
    if not private_key:
        raise ValueError("FIREBASE_PRIVATE_KEY environment variable is not set")
    if app.config.get("FIREBASE_ADMIN_CREDENTIALS"):
        cred = credentials.Certificate(app.config["FIREBASE_ADMIN_CREDENTIALS"])
    else:
        cred_dict = {
            "type": "service_account",
            "project_id": app.config["FIREBASE_CONFIG"]["projectId"],
            "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
            "private_key": private_key.replace("\\n", "\n"),
            "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
            "client_id": os.getenv("FIREBASE_CLIENT_ID"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_CERT_URL"),
        }
        cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

def login_required(f):
    """Decorator to require login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

@bp.route("/login")
def login():
    """Render login page."""
    return render_template("login.html")

@bp.route("/auth/callback")
def auth_callback():
    """Handle authentication callback from Firebase."""
    id_token = request.args.get("id_token")
    if not id_token:
        return redirect(url_for("auth.login"))
    try:
        unverified_claims = jwt.decode(id_token, options={"verify_signature": False})
        user_id = unverified_claims.get("user_id")
        name = unverified_claims.get("name")
        email = unverified_claims.get("email")
        picture = unverified_claims.get("picture")
        session["user_id"] = user_id
        session["user_name"] = name or "User"
        session["user_email"] = email or ""
        session["user_photo"] = picture or url_for(
            "static", filename="img/default-avatar.png"
        )
        session["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return redirect(url_for("main.dashboard"))
    except Exception:
        return redirect(url_for("auth.login"))

@bp.route("/logout")
def logout():
    """Handle user logout."""
    session.clear()
    return redirect(url_for("main.index"))
