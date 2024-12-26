import os
import json
from dotenv import load_dotenv

# Only load .env in development
if os.getenv('GAE_ENV', '').startswith('standard'):
    # Production in App Engine
    load_dotenv()
else:
    # Check for Render's secret file first
    render_env_path = '/etc/secrets/.env'
    if os.path.exists(render_env_path):
        load_dotenv(render_env_path)
    else:
        # Local development
        env_path = os.path.join('cursor', 'local', 'secrets', '.env')
        if not os.path.exists(env_path):
            env_path = '.env'
        load_dotenv(env_path)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-123')
    FIREBASE_CONFIG = {
        "apiKey": os.getenv('FIREBASE_API_KEY'),
        "authDomain": os.getenv('FIREBASE_AUTH_DOMAIN'),
        "projectId": os.getenv('FIREBASE_PROJECT_ID'),
        "storageBucket": os.getenv('FIREBASE_STORAGE_BUCKET'),
        "messagingSenderId": os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
        "appId": os.getenv('FIREBASE_APP_ID'),
    } 