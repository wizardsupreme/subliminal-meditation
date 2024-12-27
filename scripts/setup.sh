#!/bin/bash

# Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Install git hooks
python scripts/install_hooks.py

# Verify setup
python scripts/verify_setup.py
