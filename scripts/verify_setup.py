#!/usr/bin/env python3
"""
Verify project setup and hooks installation.
"""
import os
import sys
from hook_utils import GREEN, RESET
def verify_git_hooks():
    """Verify git hooks are properly installed."""
    git_hooks_dir = os.path.join('.git', 'hooks')
    required_hooks = {
        'commit-msg': 'Enforces conventional commit messages',
        'pre-commit': 'Checks code quality and prevents secrets',
        'post-merge': 'Auto-installs new hooks'
    }
    issues = []
    for hook, description in required_hooks.items():
        hook_path = os.path.join(git_hooks_dir, hook)
        if not os.path.exists(hook_path):
            issues.append(f"Missing hook: {hook} ({description})")
        elif not os.access(hook_path, os.X_OK):
            issues.append(f"Hook not executable: {hook}")
        return issues
def verify_dependencies():
    """Verify required Python packages are installed."""
    required = ['pylint', 'openai', 'win10toast;platform_system=="Windows"']
    issues = []
    for package in required:
        try:
            __import__(package.split(';', maxsplit=1)[0])
        except ImportError:
            issues.append(f"Missing package: {package}")
        return issues
def main():
    """Run all verifications."""
    print("🔍 Verifying project setup...")
    # Check git hooks
    print("\nChecking git hooks...")
    hook_issues = verify_git_hooks()
    if hook_issues:
        print("❌ Hook issues found:")
        for issue in hook_issues:
            print(f"  • {issue}")
        print("\nRun this to fix:")
        print("  python scripts/install_hooks.py")
    else:
        print(f"{GREEN}✓{RESET} Git hooks are properly installed")
    # Check dependencies
    print("\nChecking dependencies...")
    dep_issues = verify_dependencies()
    if dep_issues:
        print("❌ Dependency issues found:")
        for issue in dep_issues:
            print(f"  • {issue}")
        print("\nRun this to fix:")
        print("  pip install -r requirements.txt")
    else:
        print(f"{GREEN}✓{RESET} All dependencies are installed")
    # Exit with error if any issues found
    if hook_issues or dep_issues:
        sys.exit(1)
    print("\n✨ Project setup verified successfully!")
if __name__ == "__main__":
    main()
