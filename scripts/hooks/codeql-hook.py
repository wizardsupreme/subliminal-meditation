#!/usr/bin/env python3
"""
Git hook to run CodeQL analysis locally before commits.
Requires CodeQL CLI to be installed: https://github.com/github/codeql-cli-binaries
"""
import os
import subprocess
import sys
import shutil
from typing import Tuple, List
from hook_utils import GREEN, RESET, print_header, print_warning, print_success, print_info
def check_codeql_installation() -> bool:
    """Check if CodeQL CLI is installed and available."""
    try:
        subprocess.run(['codeql', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_warning("CodeQL CLI not found. Please install it from: https://github.com/github/codeql-cli-binaries")
        return False
def get_staged_files() -> List[str]:
    """Get list of staged files for analysis."""
    try:
        staged = subprocess.check_output(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            text=True
        ).splitlines()
        return [f for f in staged if f.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.c'))]
    except subprocess.CalledProcessError:
        return []
def create_database(db_path: str) -> bool:
    """Create CodeQL database for the repository."""
    try:
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        subprocess.run([
            'codeql', 'database', 'create', db_path,
            '--overwrite',  # Overwrite existing database
            '--language=python',  # Add other languages as needed
            '--source-root=.'
        ], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print_warning(f"Failed to create CodeQL database: {e}")
        return False
    except OSError as e:
        print_warning(f"Failed to create directory: {e}")
        return False
def run_analysis(db_path: str) -> Tuple[bool, str]:
    """Run CodeQL analysis using predefined queries."""
    try:
        # Run security queries from installed query pack
        query_path = os.path.expanduser(
            '~/.codeql/packages/codeql/python-queries/1.3.4/Security/CWE-078/CommandInjection.ql'
        )
        subprocess.run([
            'codeql', 'database', 'analyze', db_path,
            '--format=csv',  # Use CSV format for easier parsing
            '--output=codeql-results.csv',
            '--ram=2048',  # Limit memory usage
            '--threads=0',  # Use all available threads
            '--',  # Separate options from queries
            query_path  # Run command injection query
        ], capture_output=True, text=True, check=True)
        # Check if there are any results
        if os.path.exists('codeql-results.csv'):
            with open('codeql-results.csv', 'r', encoding='utf-8') as f:
                results = f.readlines()
                if len(results) > 1:  # More than just the header
                    return False, f"Found {len(results)-1} potential security issues:\n" + ''.join(results)
            return True, "No security issues found"
        return True, "Analysis completed successfully"
    except subprocess.CalledProcessError as e:
        return False, f"Analysis failed: {e.output}"
    finally:
        # Clean up results file
        if os.path.exists('codeql-results.csv'):
            os.remove('codeql-results.csv')
def cleanup(db_path: str):
    """Clean up temporary files and databases."""
    try:
        if os.path.exists(db_path):
            shutil.rmtree(db_path)
        if os.path.exists('codeql-results.sarif'):
            os.remove('codeql-results.sarif')
    except OSError as e:
        print_warning(f"Cleanup failed: {e}")
def main():
    """Main function to run CodeQL analysis."""
    print_header("Running CodeQL Analysis...")
    # Check if CodeQL is installed
    if not check_codeql_installation():
        sys.exit(1)
    # Get staged files
    staged_files = get_staged_files()
    if not staged_files:
        print_info("No relevant files to analyze.")
        sys.exit(0)
    # Create temporary database
    db_path = ".codeql/db"
    if not create_database(db_path):
        cleanup(db_path)
        sys.exit(1)
    # Run analysis
    success, message = run_analysis(db_path)
    cleanup(db_path)
    if not success:
        print_warning(message)
        sys.exit(1)
    print_success(message)
    print(f"\n{GREEN}✨ CodeQL analysis completed successfully!{RESET}")
if __name__ == "__main__":
    main()
