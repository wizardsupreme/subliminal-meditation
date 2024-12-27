# About

A powerful app with firebase backed authentication capabilities, built with Flask and Firebase. Uses best practices.

## 🚀 Quick Start Guide

```bash
# 1. Clone the repository
git clone https://github.com/wizardsupreme/subliminal-meditation.git
cd subliminal

# 2. Set up Python environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/MacOS

# 3. Install dependencies and set up project
python scripts/setup.sh  # This installs everything you need

# 4. Set up your environment variables
cp .env.sample .env
# Edit .env with your actual values

# 5. Configure your application
# Edit config/site_info.yaml with your app-specific settings

# 6. Run the application
python run.py
```

Visit `http://localhost:5000` to see your app running.

## 🔧 What Gets Set Up

When you run the quick start commands above, the following happens automatically:



1. All Python dependencies are installed
2. Git hooks are set up for:
   * Code quality checks (pre-commit)
   * Conventional commit messages
   * Auto-updates after pulls
3. File permissions are configured correctly
4. Basic project structure is verified

## 🎯 Features

Features are configurable in `config/site_info.yaml`. Default features include:

* 🔐 Firebase Authentication
* 📱 Responsive design
* 🎨 Modern UI with Bootstrap 5
* 🚀 Production-ready configuration

## 📁 Project Structure

```
.
├── app/                    # Main application package
│   ├── __init__.py        # App initialization
│   ├── routes/            # Application routes
│   │   ├── auth.py        # Authentication routes
│   │   └── main.py        # Main application routes
│   ├── static/            # Static files
│   │   ├── css/          # Stylesheets
│   │   ├── js/           # JavaScript files
│   │   ├── sounds/       # Meditation sounds
│   │   └── img/          # Images and icons
│   └── templates/         # Jinja2 templates
├── scripts/               # Utility scripts
│   ├── hooks/            # Git hooks
│   ├── setup.sh          # Setup script
│   ├── install_hooks.py  # Hook installer
│   └── hook_utils.py     # Hook utilities
├── config/               # Configuration files
│   └── site_info.yaml    # Site configuration
├── .env.sample          # Environment template
├── requirements.txt     # Python dependencies
└── run.py              # Application entry
```

## 🛠️ Development Setup

### Prerequisites

* Python 3.9 or higher
* Git

### Environment Variables

Copy `.env.sample` to `.env` and configure:

   ```ini
   # Flask Configuration
   FLASK_ENV=development
   FLASK_APP=run.py
   SECRET_KEY=your-secret-key

# Firebase Configuration
   FIREBASE_API_KEY=your-api-key
   FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
   FIREBASE_PROJECT_ID=your-project-id
   FIREBASE_STORAGE_BUCKET=your-bucket
   FIREBASE_MESSAGING_SENDER_ID=your-sender-id
   FIREBASE_APP_ID=your-app-id
   FIREBASE_MEASUREMENT_ID=your-measurement-id

# OpenAI Configuration (for commit messages)
OPENAI_API_KEY=your-openai-key
```

### Git Hooks

The project uses several git hooks that are automatically installed:



1. **Pre-commit Hook**
   * Checks code quality
   * Fixes line endings
   * Sets correct permissions
2. **Commit Message Hook**
   * Enforces conventional commits
   * Uses OpenAI to suggest messages
   * Example: `feat(auth): add Google sign-in`
3. **Post-merge Hook**
   * Auto-updates hooks after pulls
   * Notifies of new changes

To reinstall hooks manually:

```bash
python scripts/install_hooks.py
```

## 🚀 Git Hooks in Detail

### Installation

Git hooks are installed automatically when you run `scripts/setup.sh`. If you need to install them manually:

```bash
# Method 1: Using the install script
python scripts/install_hooks.py

# Method 2: Manual installation
cp scripts/hooks/* .git/hooks/
chmod +x .git/hooks/*  # On Unix systems
```

### How the Hooks Work



1. **Pre-commit Hook** (`scripts/hooks/pre-commit`)

   ```bash
   # Runs automatically before each commit
   # You can also run manually:
   python scripts/hooks/pre-commit
   ```
   * Checks for secrets in code
   * Fixes line endings (CRLF → LF)
   * Sets correct file permissions
   * Runs pylint on Python files
   * Auto-fixes common Python style issues
2. **Commit Message Hook** (`scripts/hooks/commit-msg`)

   ```bash
   # Runs automatically when you commit
   # To test a message manually:
   echo "your message" | python scripts/hooks/commit-msg
   ```
   * Enforces conventional commit format
   * Uses OpenAI to suggest better messages
   * Blocks commits with invalid messages
3. **Post-merge Hook** (`scripts/hooks/post-merge`)

   ```bash
   # Runs automatically after git pull/merge
   # To run manually:
   python scripts/hooks/post-merge
   ```
   * Auto-updates hooks after pulls
   * Shows desktop notifications
   * Verifies project setup

### Troubleshooting Hooks

If hooks aren't running:



1. Check they're executable: `ls -l .git/hooks/`
2. Verify installation: `python scripts/verify_setup.py`
3. Reinstall: `python scripts/install_hooks.py`

If you get "ModuleNotFoundError: No module named 'scripts'":



1. Make sure you're in the project root directory
2. Add the project root to PYTHONPATH:

   ```bash
   # Linux/MacOS
   export PYTHONPATH=$PYTHONPATH:$(pwd)
   
   # Windows PowerShell
   $env:PYTHONPATH += ";$(pwd)"
   
   # Windows CMD
   set PYTHONPATH=%PYTHONPATH%;%CD%
   ```
3. Or create a `.env` file with:

   ```ini
   PYTHONPATH=${PYTHONPATH}:${PWD}
   ```

To bypass hooks temporarily:

```bash
git commit --no-verify -m "feat: your message"
```

## 💻 Local Development

### Starting the Application

```bash
# 1. Activate your virtual environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/MacOS

# 2. Start the development server
python run.py  # Basic way
# OR with Flask debug mode
export FLASK_DEBUG=1  # Linux/MacOS
set FLASK_DEBUG=1     # Windows
flask run

# The app will be available at:
# http://localhost:5000
```

### Development Features

* **Hot Reload**: Changes to Python files trigger automatic restart
* **Debug Mode**: Detailed error pages with interactive debugger
* **Asset Compilation**: CSS/JS files are automatically recompiled

### Utility Scripts

The project includes several utility scripts for development:



1. **Avatar Setup** (`scripts/setup_avatar.py`)

   ```bash
   python scripts/setup_avatar.py
   ```
   * Sets up default avatar for users without profile pictures
   * Creates necessary directories in `app/static/img/avatars`
   * Downloads and processes a default meditation-themed avatar
   * Useful when:
     * Setting up a new development environment
     * Resetting avatars to default state
     * Testing user profile features
2. **Favicon Generation** (`scripts/create_favicon.py`)

   ```bash
   python scripts/create_favicon.py
   ```
   * Generates the app's favicon with the meditation lotus symbol
   * Creates favicons in multiple sizes (16x16, 32x32, 48x48)
   * Outputs files to `app/static/img/favicon/`:
     * `favicon.ico` - Main favicon file
     * `favicon-16x16.png` - For modern browsers
     * `favicon-32x32.png` - For high-DPI displays
     * `apple-touch-icon.png` - For iOS devices
   * Run this script when:
     * Modifying the app's branding
     * Setting up a new environment
     * Favicon files are missing or corrupted
3. **Version Management** (`scripts/manage_version.py`)

   ```bash
   # Show current version and last release date
   python scripts/manage_version.py info
   
   # Bump version (updates version.txt and git tags)
   python scripts/manage_version.py bump patch  # 1.0.0 -> 1.0.1
   python scripts/manage_version.py bump minor  # 1.0.1 -> 1.1.0
   python scripts/manage_version.py bump major  # 1.1.0 -> 2.0.0
   
   # Create a new release (combines bump and changelog)
   python scripts/manage_version.py release patch
   ```
   * Manages semantic versioning for the project
   * Updates `version.txt` automatically
   * Creates git tags for each version
   * Integrates with changelog generation
   * Use before:
     * Creating a new release
     * Deploying major features
     * Publishing to production
4. **Changelog Generation** (`scripts/generate_changelog.py`)

   ```bash
   # Generate full changelog
   python scripts/generate_changelog.py
   
   # Generate changelog for specific version
   python scripts/generate_changelog.py --version v1.0.0
   
   # Preview changelog without writing to file
   python scripts/generate_changelog.py --dry-run
   ```
   * Automatically generates CHANGELOG.md from commit history
   * Groups changes by type (features, fixes, etc.)
   * Uses conventional commits to categorize changes
   * Includes:
     * New features and enhancements
     * Bug fixes and patches
     * Breaking changes and deprecations
     * Links to related issues and PRs
   * Run this script:
     * Before creating a new release
     * After significant changes
     * When updating documentation

### Common Development Tasks

```bash
# Install new dependencies
pip install new-package
pip freeze > requirements.txt

# Run tests
python -m pytest

# Check code style
pylint app/
black app/

# Fix line endings
python scripts/fix_line_endings.py
```

## 🚀 Deployment

### Option 1: Deploy to Render (Recommended)



1. Push your code to GitHub
2. Visit [Render](https://render.com) and create a new Web Service
3. Connect your GitHub repository
4. Configure environment:
   * Build Command: `pip install -r requirements.txt`
   * Start Command: `gunicorn run:app`
   * Add all variables from your `.env`
5. Click Deploy!

### Option 2: Deploy to Your Server



1. Clone the repository on your server
2. Install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Set up environment variables
4. Run with gunicorn:

   ```bash
   gunicorn run:app
   ```

## 📝 Contributing



1. Fork the repository
2. Create your feature branch:

   ```bash
   git checkout -b feat/amazing-feature
   ```
3. Commit your changes:

   ```bash
   git commit -m "feat: add amazing feature"
   ```
4. Push to the branch:

   ```bash
   git push origin feat/amazing-feature
   ```
5. Open a Pull Request

## 📜 License

[MIT](LICENSE) - Feel free to use this project for your own purposes.

## Commit Message Convention

This project follows [Conventional Commits](https://www.conventionalcommits.org/). Each commit message should be structured as follows:

```
<type>[optional scope]: <description>
```

### Types

* `feat`: New feature
* `fix`: Bug fix
* `docs`: Documentation change
* `style`: Code style change
* `refactor`: Code refactoring
* `perf`: Performance improvement
* `test`: Adding missing tests
* `build`: Build system changes
* `ci`: CI configuration changes
* `chore`: Maintenance tasks
* `revert`: Revert a previous commit

### Examples

```
feat: add user authentication
fix(auth): handle expired tokens
docs(readme): update installation steps
style: format with black
``` 

## 🔒 CodeQL Security Analysis

The project includes local CodeQL analysis in the pre-commit hooks. This helps catch potential security issues before they're committed.

### Setting up CodeQL locally:


1. Install the CodeQL CLI:

   ```bash
   # On Windows (using Chocolatey)
   choco install codeql
   
   # On macOS (using Homebrew)
   brew install codeql
   
   # On Linux (manual installation)
   # Download from https://github.com/github/codeql-cli-binaries/releases
   # Extract and add to PATH
   ```
2. Verify installation:

   ```bash
   codeql --version
   ```

### What gets analyzed:

The CodeQL hook checks for:

* Security vulnerabilities
* Code quality issues
* Common coding mistakes
* Language-specific best practices

Currently supported languages:

* Python
* JavaScript/TypeScript
* Java
* C/C++

### Customizing CodeQL Analysis:

You can customize the analysis by modifying `scripts/hooks/codeql-hook.py`:

* Add/remove languages in the `create_database` function
* Change query suites in the `run_analysis` function
* Adjust severity thresholds
* Add custom queries

### Skipping CodeQL Analysis:

For quick commits where CodeQL analysis isn't needed:

```bash
git commit --no-verify -m "your message"
```

## 🛡️ Code Quality Standards

This repository maintains high code quality standards through automated checks and fixes. Our pre-commit hooks automatically enforce these standards before each commit.

### Coding Standards

1. **Security Best Practices** (enforced by CodeQL):
   - Prevention of SQL/Command injection vulnerabilities
   - Secure file path handling
   - Safe data deserialization
   - Proper session management
   - CSRF protection
   - Secure HTTP header handling
   - Input validation and sanitization

2. **Code Style and Quality**:
   - Automated import optimization
   - Proper line endings (LF)
   - Consistent indentation (4 spaces)
   - No unused imports or variables
   - Single newline at end of files
   - No trailing whitespace
   - Clean block structure

3. **Resource Management**:
   - Context managers for file operations
   - Secure subprocess handling
   - Proper resource cleanup
   - Exception safety

4. **Documentation**:
   - Required function docstrings
   - Type annotations
   - Parameter descriptions
   - Return type documentation

### Automated Fixes

The pre-commit hooks automatically fix common issues:

```bash
# Commit your changes
git add .
git commit -m "your message"

# The pre-commit hook will automatically:
✓ Fix code style issues
✓ Remove unused imports
✓ Fix line endings
✓ Set correct file permissions
✓ Run security checks (CodeQL)
✓ Run pylint checks
```

To skip the automated fixes (not recommended):
```bash
git commit --no-verify -m "your message"
```

### Manual Code Quality Checks

You can also run the checks manually:

```bash
# Run pylint checks
pylint app/

# Run CodeQL analysis
python scripts/hooks/codeql-hook.py

# Fix Python style issues
python scripts/hooks/pre-commit
```


