#!/bin/bash

# Create hooks directory if it doesn't exist
mkdir -p .git/hooks

# Copy commit-msg hook
cp scripts/hooks/commit-msg .git/hooks/
chmod +x .git/hooks/commit-msg

echo "Git hooks installed successfully!"
