import os
import subprocess
from datetime import datetime

import pytz
import yaml

def get_current_year():
    """Get the current year."""
    return datetime.now(pytz.UTC).year

def get_formatted_datetime():
    """Get formatted datetime with timezone."""
    # Use UTC timezone
    utc_now = datetime.now(pytz.UTC)
    return utc_now.strftime('%d.%m.%y %H:%M UTC')

def get_git_version():
    """Get version info from git."""
    # Check for production version file first
    if os.path.exists('.version'):
        with open('.version', 'r', encoding='utf-8') as f:
            version_info = yaml.safe_load(f)
            return version_info

    try:
        # Get the short SHA
        sha = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()

        # Get the latest tag if it exists
        try:
            tag = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0']).decode('ascii').strip()
            version = f"{tag}-{sha}"
        except subprocess.CalledProcessError:
            # No tags exist, just use the SHA
            version = f"dev-{sha}"

        # Get the commit date
        commit_date = subprocess.check_output(
            ['git', 'show', '-s', '--format=%ci', 'HEAD']
        ).decode('ascii').strip()

        return {
            'number': version,
            'sha': sha,
            'build_date': get_formatted_datetime(),
            'commit_date': commit_date
        }
    except Exception as e:
        print(f"Error getting git version: {e}")
        return {
            'number': 'unknown',
            'sha': 'unknown',
            'build_date': get_formatted_datetime(),
            'commit_date': 'unknown'
        }

def load_site_info():
    """Load site information from YAML config file."""
    config_path = os.path.join('config', 'site_info.yaml')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            site_info = yaml.safe_load(f)
            # Update version with git info
            site_info['version'] = get_git_version()
            # Always use current year
            site_info['company']['year'] = get_current_year()
            return site_info
    except Exception as e:
        print(f"Error loading site info: {e}")
        return {
            'company': {
                'name': 'Exponentials Studio Limited',
                'year': get_current_year()
            },
            'version': get_git_version()
        }
