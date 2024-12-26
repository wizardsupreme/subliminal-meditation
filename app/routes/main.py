from flask import Blueprint, render_template, session
from app.routes.auth import login_required

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    print(f"Accessing dashboard. User ID in session: {session.get('user_id')}")
    return render_template('dashboard.html')
