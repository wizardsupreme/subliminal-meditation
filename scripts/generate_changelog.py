"""Generate changelog entries using conventional commits and OpenAI."""
import os
import subprocess
from datetime import datetime
import re

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Configure OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_commits_since_last_tag():
    """Get all commits since the last tag."""
    try:
        # Get the last tag
        last_tag = subprocess.check_output(
            ['git', 'describe', '--tags', '--abbrev=0'],
            stderr=subprocess.DEVNULL
        ).decode('ascii').strip()

        # Get commits since last tag
        commits = subprocess.check_output(
            ['git', 'log', f'{last_tag}..HEAD', '--pretty=format:%s|%h'],
            stderr=subprocess.DEVNULL
        ).decode('ascii').strip()
    except subprocess.CalledProcessError:
        # If no tags exist, get all commits
        commits = subprocess.check_output(
            ['git', 'log', '--pretty=format:%s|%h']
        ).decode('ascii').strip()

    return commits.split('\n') if commits else []

def categorize_commits(commits):
    """Categorize commits based on conventional commit messages."""
    categories = {
        'feat': [],
        'fix': [],
        'docs': [],
        'style': [],
        'refactor': [],
        'perf': [],
        'test': [],
        'build': [],
        'ci': [],
        'chore': [],
        'other': []
    }

    for commit in commits:
        message, sha = commit.split('|')
        match = re.match(r'^(\w+)(?:\(.*?\))?: (.+)$', message)
        if match:
            type_, desc = match.groups()
            if type_ in categories:
                categories[type_].append((desc, sha))
            else:
                categories['other'].append((message, sha))
        else:
            categories['other'].append((message, sha))

    return categories

def generate_ai_summary(commits_by_category):
    """Generate an AI-powered summary of changes."""
    changes_text = ""
    for category, commits in commits_by_category.items():
        if commits:
            changes_text += f"\n{category}:\n"
            for desc, sha in commits:
                changes_text += f"- {desc} ({sha})\n"

    prompt = (
        "Given these git commits, write a concise, user-friendly changelog summary.\n"
        "Focus on the most important changes and their impact on users.\n"
        "Keep technical details minimal unless they're important for users.\n\n"
        f"Commits:\n{changes_text}\n\n"
        "Write the summary in this format:\n"
        "## What's New\n"
        "[Major new features and improvements]\n\n"
        "## Bug Fixes\n"
        "[Important fixes that affect users]\n\n"
        "## Other Changes\n"
        "[Other noteworthy changes]"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful changelog writer. "
                        "Write clear, concise summaries focused on user impact."
                    )
                },
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating AI summary: {e}")
        return None

def update_changelog(version, ai_summary, commits_by_category):
    """Update CHANGELOG.md with new entries."""
    changelog_path = 'CHANGELOG.md'
    date = datetime.now().strftime('%Y-%m-%d')

    # Prepare new content
    new_content = f"# {version} ({date})\n\n"

    if ai_summary:
        new_content += f"{ai_summary}\n\n"

    new_content += "## Detailed Changes\n\n"
    for category, commits in commits_by_category.items():
        if commits:
            new_content += f"### {category.title()}\n"
            for desc, sha in commits:
                new_content += f"- {desc} ({sha})\n"
            new_content += "\n"

    # Read existing changelog
    try:
        with open(changelog_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    except FileNotFoundError:
        existing_content = "# Changelog\n\n"

    # Combine new and existing content
    with open(changelog_path, 'w', encoding='utf-8', newline='\n') as f:
        if "# Changelog" in existing_content:
            header, rest = existing_content.split("# Changelog\n\n", 1)
            f.write(f"{header}# Changelog\n\n{new_content}{rest}")
        else:
            f.write(f"# Changelog\n\n{new_content}{existing_content}")

def main():
    """Main function to generate changelog."""
    commits = get_commits_since_last_tag()
    if not commits:
        print("No new commits found")
        return

    commits_by_category = categorize_commits(commits)
    ai_summary = generate_ai_summary(commits_by_category)

    # Get current version
    try:
        version = subprocess.check_output(
            ['git', 'describe', '--tags', '--abbrev=0'],
            stderr=subprocess.DEVNULL
        ).decode('ascii').strip()
    except subprocess.CalledProcessError:
        version = "Unreleased"

    update_changelog(version, ai_summary, commits_by_category)
    print(f"Changelog updated for version {version}")

if __name__ == "__main__":
    main()
