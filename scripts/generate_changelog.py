"""Script to generate changelog from git commits."""
from datetime import datetime
import os
import subprocess
import sys
import httpx
from dotenv import load_dotenv
from openai import OpenAI
# Load environment variables from .env file
load_dotenv()
def get_current_version():
    """Get the current version from the latest tag."""
    try:
        # Get the latest tag
        tag = subprocess.check_output(
            ['git', 'describe', '--tags', '--abbrev=0'],
            text=True
        ).strip()
        # Remove any template- prefix from existing tags for backward compatibility
        return tag.replace('template-', '')
    except subprocess.CalledProcessError:
        return "0.0.1"  # Initial version if no tags exist
def get_commits_since_last_tag():
    """Get all commits since the last tag."""
    try:
        # Get the last tag
        last_tag = subprocess.check_output(
            ['git', 'describe', '--tags', '--abbrev=0'],
            text=True
        ).strip()
        # Get commits since last tag
        return subprocess.check_output(
            ['git', 'log', f'{last_tag}..HEAD', '--pretty=format:%s'],
            text=True
        ).splitlines()
    except subprocess.CalledProcessError:
        # If no tags exist, get all commits
        return subprocess.check_output(
            ['git', 'log', '--pretty=format:%s'],
            text=True
        ).splitlines()
def categorize_commits(commits):
    """Categorize commits based on conventional commit messages."""
    categories = {
        'Features': [],
        'Bug Fixes': [],
        'Documentation': [],
        'Style': [],
        'Refactoring': [],
        'Performance': [],
        'Tests': [],
        'Build': [],
        'CI': [],
        'Chores': [],
        'Reverts': []
    }
    for commit in commits:
        if commit.startswith('feat'):
            categories['Features'].append(commit)
        elif commit.startswith('fix'):
            categories['Bug Fixes'].append(commit)
        elif commit.startswith('docs'):
            categories['Documentation'].append(commit)
        elif commit.startswith('style'):
            categories['Style'].append(commit)
        elif commit.startswith('refactor'):
            categories['Refactoring'].append(commit)
        elif commit.startswith('perf'):
            categories['Performance'].append(commit)
        elif commit.startswith('test'):
            categories['Tests'].append(commit)
        elif commit.startswith('build'):
            categories['Build'].append(commit)
        elif commit.startswith('ci'):
            categories['CI'].append(commit)
        elif commit.startswith('chore'):
            categories['Chores'].append(commit)
        elif commit.startswith('revert'):
            categories['Reverts'].append(commit)
        return {k: v for k, v in categories.items() if v}
def generate_ai_summary(commits):
    """Generate an AI-powered summary of changes."""
    if not os.getenv('OPENAI_API_KEY'):
        print("No OpenAI API key found. Skipping AI summary.", file=sys.stderr)
        return None
    print("OpenAI API key found. Generating AI summary.")
    try:
        # Initialize OpenAI client with httpx configuration
        client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            http_client=httpx.Client(
                base_url="https://api.openai.com/v1",
                timeout=60.0,
            )
        )
        # Create the completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": (
                    "Summarize these git commits in a concise paragraph:\n"
                    f"{commits}\nFocus on key changes and impact."
                )
            }],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating AI summary: {e}", file=sys.stderr)
        return None
def determine_version_bump(commits):
    """Determine how to bump the version based on conventional commits.
    Version format: MAJOR.MINOR.PATCH
    - MAJOR version for breaking changes (denoted by ! or BREAKING CHANGE)
    - MINOR version for new features (feat:)
    - PATCH version for bug fixes (fix:) and other changes
    """
    has_breaking = any('!' in commit or 'BREAKING CHANGE' in commit for commit in commits)
    has_feature = any(commit.startswith('feat:') for commit in commits)
    if has_breaking:
        return 'major'
    if has_feature:
        return 'minor'
    return 'patch'
def bump_version(current_version, bump_type):
    """Bump the version number based on SemVer rules."""
    major, minor, patch = map(int, current_version.split('.'))
    if bump_type == 'major':
        return f"{major + 1}.0.0"
    if bump_type == 'minor':
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"
def update_changelog(categories, ai_summary=None):
    """Update CHANGELOG.md with new entries."""
    commits = []
    for category_commits in categories.values():
        commits.extend(category_commits)
    current_version = get_current_version()
    bump_type = determine_version_bump(commits)
    new_version = bump_version(current_version, bump_type)
    date = datetime.now().strftime('%Y-%m-%d')
    content = f"## [{new_version}] - {date}\n\n"
    if ai_summary:
        content += f"### Summary\n{ai_summary}\n\n"
    for category, category_commits in categories.items():
        if category_commits:
            content += f"### {category}\n"
            for commit in category_commits:
                content += f"- {commit}\n"
            content += "\n"
        # Read existing changelog
    try:
        with open('CHANGELOG.md', 'r', encoding='utf-8') as f:
            old_content = f.read()
    except FileNotFoundError:
        changelog_header = (
            "# Changelog\n\n"
            "All notable changes to this project will be documented in this file.\n\n"
        )
        return changelog_header + content
        # Insert new changes after the header
    header_end = old_content.find('\n\n')
    if header_end == -1:
        header_end = len(old_content)
    # Create new content by combining old and new
    return old_content[:header_end + 2] + content + old_content[header_end + 2:]
def main():
    """Main function to generate changelog."""
    commits = get_commits_since_last_tag()
    if not commits:
        print("No new commits to add to changelog")
        return
    categories = categorize_commits(commits)
    ai_summary = generate_ai_summary('\n'.join(commits))
    new_content = update_changelog(categories, ai_summary)
    with open('CHANGELOG.md', 'w', encoding='utf-8', newline='\n') as f:
        f.write(new_content)
    # Create a new tag with the bumped version
    current_version = get_current_version()
    bump_type = determine_version_bump(commits)
    new_version = bump_version(current_version, bump_type)
    try:
        # Create tag without template- prefix
        subprocess.run(['git', 'tag', new_version, '-m', f'Version {new_version}'], check=True)
        print(f"Created new tag: {new_version}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating tag: {e}", file=sys.stderr)
    print("Successfully updated CHANGELOG.md")
if __name__ == '__main__':
    main()
