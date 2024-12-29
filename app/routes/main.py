"""Main application routes."""
from flask import Blueprint, render_template
from app.routes.auth import login_required

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    """Render the dashboard page."""
    return render_template('dashboard.html')
