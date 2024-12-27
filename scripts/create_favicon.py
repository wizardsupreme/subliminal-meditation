from pathlib import Path
from PIL import Image, ImageDraw

def create_lotus_icon(size):
    """Create a lotus icon with the given size."""
    # Create a new image with transparent background
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    # Purple color matching the navbar icon
    color = '#7C4DFF'
    # Calculate center and radius
    center = size // 2
    radius = size // 3
    # Draw a simplified lotus shape
    # Draw petals as circles arranged in a flower pattern
    for angle in range(0, 360, 60):
        x = center + int(radius * 0.7 * (angle / 360))
        y = center + int(radius * 0.7 * ((angle + 30) / 360))
        draw.ellipse([x - radius//2, y - radius//2, x + radius//2, y + radius//2], fill=color)
    # Draw center circle
    draw.ellipse([center - radius//3, center - radius//3,
                 center + radius//3, center + radius//3], fill=color)
    return image

# Create directories if they don't exist
favicon_dir = Path('app/static/img/favicon')
favicon_dir.mkdir(parents=True, exist_ok=True)

# Create favicons in different sizes
sizes = [16, 32, 180]
for size in sizes:
    img = create_lotus_icon(size)
    output_file = favicon_dir / f'favicon-{size}x{size}.png'
    if size == 180:
        output_file = favicon_dir / 'apple-touch-icon.png'
    img.save(output_file, 'PNG')

# Create ICO file
ico_img = create_lotus_icon(16)
ico_img.save(favicon_dir.parent / 'favicon.ico', format='ICO', sizes=[(16, 16)])

print("Favicons created successfully!")
