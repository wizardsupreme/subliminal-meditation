#!/usr/bin/env python3
"""
Version management script for the application.
Usage:
    python scripts/manage_version.py bump [major|minor|patch]
    python scripts/manage_version.py tag
    python scripts/manage_version.py info
"""

import subprocess
import sys
import re
from datetime import datetime

def get_current_version():
    """Get the current version from the latest tag."""
    try:
        tag = subprocess.check_output(
            ['git', 'describe', '--tags', '--abbrev=0'],
            stderr=subprocess.DEVNULL
        ).decode('ascii').strip()
        # Extract version numbers
        match = re.match(r'v?(\d+)\.(\d+)\.(\d+)', tag)
        if match:
            return tuple(map(int, match.groups()))
        return (0, 0, 0)
    except subprocess.CalledProcessError:
        return (0, 0, 0)

def bump_version(current_version, bump_type):
    """Bump the version number based on semver."""
    major, minor, patch = current_version
    if bump_type == 'major':
        return (major + 1, 0, 0)
    if bump_type == 'minor':
        return (major, minor + 1, 0)
    # patch
    return (major, minor, patch + 1)

def create_tag(version):
    """Create and push a new git tag."""
    tag = f'v{".".join(map(str, version))}'
    message = f'Release {tag} - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'

    try:
        # Create tag
        subprocess.run(['git', 'tag', '-a', tag, '-m', message], check=True)
        print(f'Created tag: {tag}')

        # Push tag
        push = input('Push tag to remote? [y/N] ').lower()
        if push == 'y':
            subprocess.run(['git', 'push', 'origin', tag], check=True)
            print(f'Pushed tag {tag} to remote')
    except subprocess.CalledProcessError as e:
        print(f'Error creating tag: {e}')

def show_version_info():
    """Display current version information."""
    try:
        # Get latest tag
        current = subprocess.check_output(
            ['git', 'describe', '--tags', '--abbrev=0'],
            stderr=subprocess.DEVNULL
        ).decode('ascii').strip()
    except subprocess.CalledProcessError:
        current = 'No tags'

    # Get commit info
    sha = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
    commit_date = subprocess.check_output(
        ['git', 'show', '-s', '--format=%ci', 'HEAD']
    ).decode('ascii').strip()

    print(f'''
Version Information:
-------------------
Current Tag: {current}
Commit SHA: {sha}
Commit Date: {commit_date}
    ''')

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == 'bump':
        if len(sys.argv) != 3 or sys.argv[2] not in ['major', 'minor', 'patch']:
            print('Please specify bump type: major, minor, or patch')
            sys.exit(1)

        current = get_current_version()
        new_version = bump_version(current, sys.argv[2])
        create_tag(new_version)

    elif command == 'tag':
        current = get_current_version()
        create_tag(current)

    elif command == 'info':
        show_version_info()

    else:
        print('Unknown command. Use bump, tag, or info')
        sys.exit(1)

if __name__ == '__main__':
    main()
