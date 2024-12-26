import os
import base64
import requests  # Import at top level

def setup_default_avatar():
    """Set up the default avatar for users without profile pictures."""
    img_dir = os.path.join('app', 'static', 'img')
    os.makedirs(img_dir, exist_ok=True)

    # Path to default avatar
    avatar_path = os.path.join(img_dir, 'default-avatar.png')

    # Only download if file doesn't exist
    if not os.path.exists(avatar_path):
        print("Downloading default avatar...")
        try:
            url = "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y&s=200"
            response = requests.get(url, timeout=10)  # Add timeout
            response.raise_for_status()
            with open(avatar_path, 'wb') as f:
                f.write(response.content)
            print("Default avatar downloaded successfully!")
        except Exception as e:
            print(f"Error downloading avatar: {e}")
            create_default_avatar(avatar_path)
    else:
        print("Default avatar already exists!")

def create_default_avatar(path):
    """Create a default avatar from base64 string."""
    try:
        with open(path, 'wb') as f:
            f.write(base64.b64decode(DEFAULT_AVATAR_BASE64))
        print("Created default avatar from base64 backup")
    except Exception as e:
        print(f"Error creating avatar from base64: {e}")

# Move long string to constant at module level
DEFAULT_AVATAR_BASE64 = '''
iVBORw0KGgoAAAANSUhEUgAAAMAAAADACAYAAABS3GwHAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAA12SURBVHic7Z15kFxVHcc/r2d2k91sks1uQhKSkBASwqEECKDhUFBQKQG5tBAqgIhSXCWCQimUB4cWYgk...
'''

if __name__ == "__main__":
    setup_default_avatar()
