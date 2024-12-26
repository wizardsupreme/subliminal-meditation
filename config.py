import os
import json
from dotenv import load_dotenv

# Only load .env in development
if os.getenv('GAE_ENV', '').startswith('standard'):
    # Production in App Engine
    load_dotenv()
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
    
    # In production, construct credentials from environment variables
    if os.getenv('FIREBASE_PRIVATE_KEY'):
        FIREBASE_ADMIN_CREDENTIALS = {
            "type": "service_account",
            "project_id": os.getenv('FIREBASE_PROJECT_ID'),
            "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
            "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
            "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
            "client_id": os.getenv('FIREBASE_CLIENT_ID'),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_CERT_URL')
        }
    else:
        FIREBASE_ADMIN_SDK_PATH = 'firebase-admin-sdk.json' 