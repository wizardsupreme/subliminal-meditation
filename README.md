# Flask Application Template with Firebase Auth

A production-ready Flask application template with Firebase Authentication, ready to deploy on Render.

## Quick Start with Cursor

1. **Create from Template**
   - Visit [Flask-Firebase-Template](https://github.com/yourusername/flask-firebase-template)
   - Click "Use this template" button
   - Name your repository and create it

2. **Open in Cursor**
   - Open Cursor
   - Select "Clone Repository"
   - Paste your new repository URL

3. **Useful Prompts for Cursor AI**
   ```
   "Help me set up Firebase configuration for this app"
   "Add a new protected route for [your feature]"
   "Create a new template page for [your feature]"
   "Help me style the [component] using Bootstrap"
   "Add form validation to [form name]"
   ```

## Features

- 🔐 Firebase Authentication (Google Sign-in)
- 🚀 Ready to deploy on Render
- 🎨 Bootstrap 5 + Font Awesome
- 🔒 Environment variables configuration
- 🖼️ Default avatar handling
- 📱 Responsive design

## Project Structure
```
.
├── app/
│   ├── __init__.py          # App initialization
│   ├── routes/
│   │   ├── auth.py          # Authentication routes
│   │   └── main.py          # Main application routes
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Custom styles
│   │   ├── js/
│   │   │   └── main.js      # Custom JavaScript
│   │   └── img/
│   │       ├── favicon.ico   # Site favicon
│   │       └── default-avatar.png
│   └── templates/
│       ├── base.html        # Base template
│       ├── index.html       # Landing page
│       ├── login.html       # Login page
│       └── dashboard.html   # User dashboard
├── config.py                # Configuration settings
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── runtime.txt             # Python version
└── render.yaml             # Render deployment config
```

## Setup Instructions

1. **Firebase Setup**
   - Create project at [Firebase Console](https://console.firebase.google.com)
   - Enable Google Authentication:
     - Go to Authentication → Sign-in method
     - Enable Google sign-in
   - Create Web App:
     - Click gear icon → Project settings
     - Add web app (</>)
     - Register app and copy config
   - Get Admin SDK credentials:
     - Go to Project settings → Service accounts
     - Generate new private key

2. **Environment Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate it
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Environment Variables**
   Create `.env` file with:
   ```ini
   # Flask Configuration
   FLASK_ENV=development
   FLASK_APP=run.py
   SECRET_KEY=your-secret-key

   # Firebase Web Configuration
   FIREBASE_API_KEY=your-api-key
   FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
   FIREBASE_PROJECT_ID=your-project-id
   FIREBASE_STORAGE_BUCKET=your-bucket
   FIREBASE_MESSAGING_SENDER_ID=your-sender-id
   FIREBASE_APP_ID=your-app-id
   FIREBASE_MEASUREMENT_ID=your-measurement-id

   # Firebase Admin SDK Configuration
   FIREBASE_PRIVATE_KEY_ID=your-private-key-id
   FIREBASE_PRIVATE_KEY="your-private-key"
   FIREBASE_CLIENT_EMAIL=your-client-email
   FIREBASE_CLIENT_ID=your-client-id
   FIREBASE_CLIENT_CERT_URL=your-cert-url
   ```

## Deployment to Render

1. Push your code to GitHub
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Add environment variables:
   - Go to Dashboard → Environment
   - Add all variables from your `.env` file
5. Deploy!

## Common Customizations

### Adding a New Feature
1. Create route in `app/routes/your_feature.py`:
   ```python
   from flask import Blueprint, render_template
   from app.routes.auth import login_required

   bp = Blueprint('your_feature', __name__)

   @bp.route('/your-feature')
   @login_required
   def your_feature():
       return render_template('your_feature.html')
   ```

2. Register in `app/__init__.py`:
   ```python
   from app.routes import your_feature
   app.register_blueprint(your_feature.bp)
   ```

3. Create template in `app/templates/your_feature.html`:
   ```html
   {% extends "base.html" %}
   {% block content %}
     <!-- Your content here -->
   {% endblock %}
   ```

## Contributing

Pull requests are welcome! For major changes, please open an issue first.

## License

[MIT](https://choosealicense.com/licenses/mit/) 