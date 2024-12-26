#!/bin/bash

# Install pylint
pip install pylint

# Install pre-commit
pip install pre-commit

# Install the git hook scripts
pre-commit install

# Update hooks to the latest version
pre-commit autoupdate
