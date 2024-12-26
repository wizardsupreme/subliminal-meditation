import os
from dotenv import load_dotenv

load_dotenv()

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
    FIREBASE_ADMIN_SDK_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'subliminal/firebase-admin-sdk.json') 