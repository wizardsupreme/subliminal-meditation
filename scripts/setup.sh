python -m pip install --upgrade pip
pip install -r requirements.txt

# Install git hooks
bash scripts/install_hooks.sh

# Verify setup
python scripts/verify_setup.py
