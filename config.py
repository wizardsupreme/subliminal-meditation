import os
from dotenv import load_dotenv

# Try to load from cursor local secrets first, fall back to regular .env
env_path = os.path.join('cursor', 'local', 'secrets', '.env')
if not os.path.exists(env_path):
    env_path = '.env'
load_dotenv(env_path)

class Config:
    SECRET_KEY = 'a-long-random-string-used-as-secret-key-12345'
    FIREBASE_CONFIG = {
        "apiKey": os.getenv('FIREBASE_API_KEY'),
        "authDomain": os.getenv('FIREBASE_AUTH_DOMAIN'),
        "projectId": os.getenv('FIREBASE_PROJECT_ID'),
        "storageBucket": os.getenv('FIREBASE_STORAGE_BUCKET'),
        "messagingSenderId": os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
        "appId": os.getenv('FIREBASE_APP_ID'),
    }
    # Look for Firebase admin SDK in cursor local secrets first
    sdk_path = os.path.join('cursor', 'local', 'secrets', 'firebase-admin-sdk.json')
    if not os.path.exists(sdk_path):
        sdk_path = 'firebase-admin-sdk.json'
    FIREBASE_ADMIN_SDK_PATH = sdk_path 