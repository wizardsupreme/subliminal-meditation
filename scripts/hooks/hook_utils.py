"""Utility functions for git hooks."""
import os
import sys
import subprocess
from typing import Optional
# ANSI color codes
GREEN = '\033[92m'      # Success
RED = '\033[91m'        # Error
YELLOW = '\033[93m'     # Warning
BLUE = '\033[94m'       # Info
MAGENTA = '\033[95m'    # Special
CYAN = '\033[96m'       # Debug
BOLD = '\033[1m'        # Bold
RESET = '\033[0m'       # Reset
def print_success(message: str) -> None:
    """Print a success message with green checkmark."""
    print(f"{GREEN}✓{RESET} {message}")
def print_error(message: str) -> None:
    """Print an error message with red X."""
    print(f"{RED}✗{RESET} {message}")
def print_warning(message: str) -> None:
    """Print a warning message with yellow exclamation."""
    print(f"{YELLOW}!{RESET} {message}")
def print_info(message: str) -> None:
    """Print an info message with blue dot."""
    print(f"{BLUE}•{RESET} {message}")
def print_special(message: str) -> None:
    """Print a special message with magenta star."""
    print(f"{MAGENTA}★{RESET} {message}")
def print_debug(message: str) -> None:
    """Print a debug message with cyan arrow."""
    print(f"{CYAN}→{RESET} {message}")
def print_header(message: str) -> None:
    """Print a bold header message."""
    print(f"\n{BOLD}{message}{RESET}")
def format_path(path: str) -> str:
    """Format a path with cyan color."""
    return f"{CYAN}{path}{RESET}"
def format_command(cmd: str) -> str:
    """Format a command with magenta color."""
    return f"{MAGENTA}{cmd}{RESET}"
def find_python() -> Optional[str]:
    """Find the Python executable to use."""
    # Try environment Python first
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        return sys.executable
    # Try common Python commands
    for cmd in ['python', 'python3', 'py']:
        try:
            subprocess.run([cmd, '--version'], check=True, capture_output=True)
            return cmd
        except (subprocess.SubprocessError, FileNotFoundError):
            continue
        return None
def get_repo_root() -> str:
    """Get the root directory of the git repository."""
    try:
        return subprocess.check_output(
            ['git', 'rev-parse', '--show-toplevel'],
            text=True
        ).strip()
    except subprocess.SubprocessError:
        return os.getcwd()
