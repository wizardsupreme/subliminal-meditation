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
files_to_fix = [
    'app/__init__.py',
    'app/routes/auth.py',
    'app/routes/main.py',
    'config.py',
    'run.py',
    'scripts/create_favicon.py',
    'scripts/setup_avatar.py',
    'setup_avatar.py'
]

for file in files_to_fix:
    try:
        normalize_line_endings(file)
        print(f"Fixed line endings in {file}")
    except Exception as e:
        print(f"Error fixing {file}: {e}")
