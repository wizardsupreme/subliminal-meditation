#!/usr/bin/env python3
"""
Git hook to run CodeQL analysis locally before commits.
Requires CodeQL CLI to be installed: https://github.com/github/codeql-cli-binaries
"""
import os
import subprocess
import sys
from typing import Tuple, List
from hook_utils import GREEN, RESET, RED, YELLOW, print_header, print_warning, print_success, print_info

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
        subprocess.run([
            'codeql', 'database', 'create', db_path,
            '--language=python',  # Add other languages as needed
            '--source-root=.'
        ], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print_warning(f"Failed to create CodeQL database: {e}")
        return False

def run_analysis(db_path: str) -> Tuple[bool, str]:
    """Run CodeQL analysis using predefined queries."""
    try:
        # Run security queries from CodeQL standard suite
        result = subprocess.run([
            'codeql', 'database', 'analyze', db_path,
            'security-and-quality.qls',  # Standard security and quality suite
            '--format=sarif-latest',
            '--output=codeql-results.sarif'
        ], capture_output=True, text=True, check=True)
        
        # Parse and format results
        if os.path.exists('codeql-results.sarif'):
            # TODO: Parse SARIF file and format results nicely
            return True, "Analysis completed successfully"
        return True, "No issues found"
    except subprocess.CalledProcessError as e:
        return False, f"Analysis failed: {e.output}"

def cleanup(db_path: str):
    """Clean up temporary files and databases."""
    try:
        if os.path.exists(db_path):
            subprocess.run(['rm', '-rf', db_path], check=True)
        if os.path.exists('codeql-results.sarif'):
            os.remove('codeql-results.sarif')
    except (subprocess.CalledProcessError, OSError) as e:
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