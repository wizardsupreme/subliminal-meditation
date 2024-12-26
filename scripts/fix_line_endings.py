def normalize_line_endings(filename):
    """Convert CRLF to LF in the given file."""
    with open(filename, 'rb') as f:
        content = f.read()
    content = content.replace(b'\r\n', b'\n')
    with open(filename, 'wb') as f:
        f.write(content)

# Files to fix
files_to_fix = [
    'scripts/create_favicon.py',
    '.pylintrc',
    'app/routes/auth.py',
    'app/routes/main.py',
    'app/__init__.py',
    'config.py',
    'run.py'
]

for file in files_to_fix:
    try:
        normalize_line_endings(file)
        print(f"Fixed line endings in {file}")
    except Exception as e:
        print(f"Error fixing {file}: {e}")
