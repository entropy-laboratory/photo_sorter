from pathlib import Path
import shutil
import colorsys
from PIL import Image
import numpy as np

# Settings
reverse_sort = False  # Set to True to sort from 1.0 to 0.0 (descending)

# Determine script's base directory dynamically
base_dir = Path(__file__).resolve().parent
folder_path = base_dir / "photo_source"  # Folder with source images
output_folder = folder_path / 'HUEsorted'  # Output folder for sorted images

# Create output folder if it doesn't exist
output_folder.mkdir(parents=True, exist_ok=True)

# Function to calculate the average color and convert it to HSV
def get_average_hue(image_path):
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        img = img.resize((100, 100))  # Speed up processing
        np_img = np.array(img)
        avg_color = np.mean(np_img, axis=(0, 1))
        r, g, b = avg_color / 255.0
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return h, s, v

# Collect all image files
images = [f for f in folder_path.iterdir() if f.suffix.lower() in ('.png', '.jpg', '.jpeg')]

# Compute average hue for each image
image_colors = []
for img_path in images:
    try:
        hue, sat, val = get_average_hue(img_path)
        image_colors.append((img_path, hue, sat, val))
    except Exception as e:
        print(f'Error with {img_path.name}: {e}')

# Sort by hue, with optional reverse
sorted_images = sorted(image_colors, key=lambda x: x[1], reverse=reverse_sort)

# Display and copy sorted images
debug_list = []
direction_text = "ascending (from 0.0 to 1.0)" if not reverse_sort else "descending (from 1.0 to 0.0)"
print(f'Suggested image order by Hue ({direction_text}):')

for i, (img_path, hue, sat, val) in enumerate(sorted_images, 1):
    new_name = f'{i * 100:05d}_{img_path.name}'
    print(f'{new_name} - Hue: {hue:.2f}')
    dst_path = output_folder / new_name
    shutil.copy2(img_path, dst_path)
    debug_list.append(f'{new_name} - Hue: {hue:.2f}')

# Save order to text file
with open(output_folder / 'sorted_image_list.txt', 'w') as f:
    for line in debug_list:
        f.write(line + '\n')

print(f'\nImages have been copied to {output_folder.resolve()} in sorted order.')
