"""Script to install git hooks."""
import os
import shutil
import stat
from typing import Dict
import platform
import sys
# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'
# Description of what each hook does
HOOK_DESCRIPTIONS: Dict[str, str] = {
    'pre-commit': 'Checks code quality, secrets, and fixes issues',
    'commit-msg': 'Validates commit message format',
    'post-merge': 'Auto-installs new hooks after pull/merge',
}
def print_success(message: str) -> None:
    """Print a success message with green checkmark."""
    print(f"{GREEN}✓{RESET} {message}")
def print_error(message: str) -> None:
    """Print an error message with red X."""
    print(f"{RED}✗{RESET} {message}")
def discover_hooks() -> Dict[str, str]:
    """Discover all available hooks in the hooks directory."""
    hooks_dir = os.path.join('scripts', 'hooks')
    available_hooks = {}
    if not os.path.exists(hooks_dir):
        print_error(f"Hooks directory not found: {hooks_dir}")
        return available_hooks
    for filename in os.listdir(hooks_dir):
        filepath = os.path.join(hooks_dir, filename)
        if os.path.isfile(filepath) and filename in HOOK_DESCRIPTIONS:
            available_hooks[filename] = HOOK_DESCRIPTIONS[filename]
        return available_hooks
def install_hooks() -> None:
    """Install git hooks to the project."""
    git_hooks_dir = os.path.join('.git', 'hooks')
    os.makedirs(git_hooks_dir, exist_ok=True)
    available_hooks = discover_hooks()
    if not available_hooks:
        print_error("No hooks found to install!")
        return
    print(f"\nFound {BOLD}{len(available_hooks)}{RESET} hooks to install:")
    for hook_name, description in available_hooks.items():
        print(f"  • {hook_name}: {description}")
    # Install each hook
    for hook_name in available_hooks:
        source = os.path.join('scripts', 'hooks', hook_name)
        destination = os.path.join(git_hooks_dir, hook_name)
        try:
            print(f"\nInstalling {hook_name}...")
            if platform.system() == 'Windows':
                with open(destination, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(f'#!/bin/sh\n"{sys.executable}" "{os.path.abspath(source)}" "$@"')
            else:
                shutil.copy2(source, destination)
                st = os.stat(destination)
                os.chmod(destination, st.st_mode | stat.S_IEXEC)
                print_success(f"{hook_name} installed successfully")
        except Exception as e:
            print_error(f"Error installing {hook_name}: {e}")
            # Set permissions for all script files
        print("\nSetting script permissions...")
    executable_patterns = [
        '*.sh',
        'scripts/*/*.py',
        'scripts/*.py'
    ]
    for pattern in executable_patterns:
        try:
            files = os.popen(f'git ls-files {pattern}').read().splitlines()
            for file in files:
                if os.path.exists(file):
                    st = os.stat(file)
                    os.chmod(file, st.st_mode | 0o755)  # rwxr-xr-x
                    print_success(f"Set permissions for {file}")
        except Exception as e:
            print_error(f"Error setting permissions for {pattern}: {e}")
def main() -> None:
    """Main function to install hooks."""
    try:
        install_hooks()
        print(f"\n{GREEN}✨ Hook installation completed!{RESET}")
    except Exception as e:
        print(f"\n{RED}❌ Error during hook installation: {e}{RESET}")
        raise
if __name__ == "__main__":
    main()
