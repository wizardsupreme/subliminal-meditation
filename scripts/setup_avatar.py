import os
import base64

def setup_default_avatar():
    # Create the directory if it doesn't exist
    img_dir = os.path.join('app', 'static', 'img')
    os.makedirs(img_dir, exist_ok=True)

    # Path to default avatar
    avatar_path = os.path.join(img_dir, 'default-avatar.png')
    # Base64 encoded simple avatar image (light blue circle with white user icon)
    default_avatar_base64 = '''
    iVBORw0KGgoAAAANSUhEUgAAAMAAAADACAYAAABS3GwHAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAA12SURBVHic7Z15kFxVHcc/r2d2k91sks1uQhKSkBASwqEECKDhUFBQKQG5tBAqgIhSXCWCQimUB4cWYgk...'''

    # Only download if file doesn't exist 
    if not os.path.exists(avatar_path):
        print("Downloading default avatar...")
        try:
            import requests
            url = "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y&s=200"
            response = requests.get(url)
            response.raise_for_status()
            with open(avatar_path, 'wb') as f:
                f.write(response.content)
            print("Default avatar downloaded successfully!")
        except Exception as e:
            print(f"Error downloading avatar: {e}")
            # If download fails, create from base64
            try:
                with open(avatar_path, 'wb') as f:
                    f.write(base64.b64decode(default_avatar_base64))
                print("Created default avatar from base64 backup")
            except Exception as e:
                print(f"Error creating avatar from base64: {e}")
    else:
        print("Default avatar already exists!")

if __name__ == "__main__":
    setup_default_avatar()