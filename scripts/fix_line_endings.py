"""Script to fix line endings in project files."""
import os.path  # More specific import for what we actually use

def normalize_line_endings(filename):
    """Convert CRLF to LF in the given file and ensure final newline."""
    with open(filename, 'rb') as f:
        content = f.read()
    content = content.replace(b'\r\n', b'\n')
    if not content.endswith(b'\n'):
        content += b'\n'
    with open(filename, 'wb') as f:
        f.write(content)

# Files to fix
FILES_TO_FIX = [
    os.path.join('app', '__init__.py'),
    os.path.join('app', 'routes', 'auth.py'),
    os.path.join('app', 'routes', 'main.py'),
    'config.py',
    'run.py',
    os.path.join('scripts', 'create_favicon.py'),
    os.path.join('scripts', 'setup_avatar.py'),
    'setup_avatar.py'
]

def main():
    """Main function to fix line endings."""
    for file in FILES_TO_FIX:
        try:
            normalize_line_endings(file)
            print(f"Fixed line endings in {file}")
        except Exception as e:
            print(f"Error fixing {file}: {e}")

if __name__ == "__main__":
    main()
