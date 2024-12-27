"""Script to install git hooks."""
import os
import shutil
import stat

HOOKS = {
    'commit-msg': 'Conventional commit message validator',
    'pre-commit': 'Line endings and permissions checker'
}

def install_hooks():
    """Install git hooks to the project."""
    # Create hooks directory if it doesn't exist
    hooks_dir = os.path.join('.git', 'hooks')
    os.makedirs(hooks_dir, exist_ok=True)

    # Install each hook
    for hook_name, description in HOOKS.items():
        source = os.path.join('scripts', 'hooks', hook_name)
        destination = os.path.join(hooks_dir, hook_name)

        try:
            print(f"Installing {hook_name} hook ({description})...")
            shutil.copy2(source, destination)

            # Make the hook executable
            st = os.stat(destination)
            os.chmod(destination, st.st_mode | stat.S_IEXEC)

            print(f"✓ {hook_name} installed successfully")
        except Exception as e:
            print(f"✗ Error installing {hook_name}: {e}")

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
                    print(f"✓ Set permissions for {file}")
        except Exception as e:
            print(f"✗ Error setting permissions for {pattern}: {e}")

if __name__ == "__main__":
    install_hooks()
