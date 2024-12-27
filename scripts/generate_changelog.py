"""Generate changelog entries using conventional commits and OpenAI."""
import os
import sys
import subprocess
from datetime import datetime
from openai import OpenAI
def get_commits_since_last_tag():
    """Get all commits since the last tag."""
    try:
        # Get the last tag
        last_tag = subprocess.check_output(
            ['git', 'describe', '--tags', '--abbrev=0'],
            text=True
        ).strip()
    except subprocess.CalledProcessError:
        # If no tags exist, get all commits
        return subprocess.check_output(
            ['git', 'log', '--pretty=format:%s'],
            text=True
        ).splitlines()
    # Get commits since last tag
    return subprocess.check_output(
        ['git', 'log', f'{last_tag}..HEAD', '--pretty=format:%s'],
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
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("No OpenAI API key found. Skipping AI summary.", file=sys.stderr)
        return None
    try:
        client = OpenAI()  # The API key will be read from environment variable
        prompt = f"""Summarize the following git commits in a concise paragraph:
        {commits}
    Focus on the key changes and their impact. Keep it brief but informative."""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating AI summary: {e}", file=sys.stderr)
        return None
def update_changelog(categories, ai_summary=None):
    """Update CHANGELOG.md with new entries."""
    date = datetime.now().strftime('%Y-%m-%d')
    content = f"## [{date}]\n\n"
    if ai_summary:
        content += f"### Summary\n{ai_summary}\n\n"
    for category, commits in categories.items():
        if commits:
            content += f"### {category}\n"
            for commit in commits:
                content += f"- {commit}\n"
            content += "\n"
        # Read existing changelog
    try:
        with open('CHANGELOG.md', 'r', encoding='utf-8') as f:
            old_content = f.read()
    except FileNotFoundError:
        old_content = "# Changelog\n\nAll notable changes to this project will be documented in this file.\n\n"
        # Insert new changes after the header
    header_end = old_content.find('\n\n')
    if header_end == -1:
        header_end = len(old_content)
    new_content = old_content[:header_end + 2] + content + old_content[header_end + 2:]
    # Write updated changelog
    with open('CHANGELOG.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
def main():
    """Main function to generate changelog."""
    commits = get_commits_since_last_tag()
    if not commits:
        print("No new commits to add to changelog")
        return
    categories = categorize_commits(commits)
    ai_summary = generate_ai_summary('\n'.join(commits))
    update_changelog(categories, ai_summary)
    print("Successfully updated CHANGELOG.md")
if __name__ == '__main__':
    main()
