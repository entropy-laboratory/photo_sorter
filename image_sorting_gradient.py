import os
import shutil
import numpy as np
from PIL import Image
import cv2
from sklearn.cluster import KMeans
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import pandas as pd

# Automatically determine paths based on script location
base_dir = os.path.dirname(os.path.abspath(__file__))
source_folder = os.path.join(base_dir, "input")
destination_folder = os.path.join(base_dir, "output", "sortedNEWMETHOD")

# Create destination folders if they don't exist
os.makedirs(destination_folder, exist_ok=True)
gradient_folder = os.path.join(destination_folder, "gradient")
os.makedirs(gradient_folder, exist_ok=True)

# Define category labels
categories = {
    "vibrant": "01_vibrant",
    "pastel": "02_pastel",
    "monochrome": "03_monochrome",
    "dark": "04_dark",
    "nature": "05_nature",
    "urban": "06_urban",
    "portrait": "07_portrait",
    "abstract": "08_abstract",
    "other": "09_other"
}

# Feature extraction from an image
def get_image_features(image_path, n_colors=5):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resized_img = cv2.resize(img, (100, 100))
    pixels = resized_img.reshape(-1, 3)

    kmeans = KMeans(n_clusters=n_colors, random_state=0).fit(pixels)
    colors = kmeans.cluster_centers_
    labels = kmeans.labels_
    count = Counter(labels)
    sorted_colors = [colors[i] for i in count.keys()]
    percentages = [count[i] / len(labels) for i in count.keys()]

    hist_features = []
    for i in range(3):
        channel_hist, _ = np.histogram(resized_img[:,:,i], bins=8, range=(0, 256))
        hist_features.extend(channel_hist / np.sum(channel_hist))

    brightness = np.mean(resized_img) / 255.0
    hsv_img = cv2.cvtColor(resized_img, cv2.COLOR_RGB2HSV)
    saturation = np.mean(hsv_img[:, :, 1]) / 255.0

    gray = cv2.cvtColor(resized_img, cv2.COLOR_RGB2GRAY)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist = hist / np.sum(hist)
    entropy = -np.sum(hist * np.log2(hist + 1e-10))

    edges = cv2.Canny(gray, 100, 200)
    edge_percentage = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])

    dominant_color = sorted_colors[0] if sorted_colors else np.array([0, 0, 0])

    features = {
        'dominant_r': dominant_color[0] / 255.0,
        'dominant_g': dominant_color[1] / 255.0,
        'dominant_b': dominant_color[2] / 255.0,
        'brightness': brightness,
        'saturation': saturation,
        'entropy': entropy / 8.0,
        'edge_density': edge_percentage
    }

    for i, hist_val in enumerate(hist_features):
        features[f'hist_{i}'] = hist_val

    return features, sorted_colors, percentages

# Heuristic category detection functions (omitted for brevity)

def determine_category(image_path, features, colors, percentages):
    return "other"  # Placeholder, assumes all images are 'other' for this example

# Main function for analyzing and sorting images
def analyze_and_sort_images():
    supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    image_files = [f for f in os.listdir(source_folder)
                   if os.path.isfile(os.path.join(source_folder, f))
                   and f.lower().endswith(supported_extensions)]

    print(f"Found {len(image_files)} images to process.")

    all_features = []
    image_data = []
    categories_count = {category: 0 for category in categories}

    for idx, image_file in enumerate(image_files):
        try:
            image_path = os.path.join(source_folder, image_file)
            features, colors, percentages = get_image_features(image_path)
            category = determine_category(image_path, features, colors, percentages)

            all_features.append(features)
            image_data.append({
                'file': image_file,
                'path': image_path,
                'category': category
            })
            categories_count[category] += 1

            print(f"{idx+1}/{len(image_files)}: {image_file} -> {category}")
        except Exception as e:
            print(f"Error for {image_file}: {e}")

    features_df = pd.DataFrame(all_features)
    pca = PCA(n_components=1)
    gradient_values = pca.fit_transform(features_df)
    gradient_norm = (gradient_values - gradient_values.min()) / (gradient_values.max() - gradient_values.min())

    for i, img_data in enumerate(image_data):
        img_data['gradient_value'] = float(gradient_norm[i])

    image_data.sort(key=lambda x: x['gradient_value'])

    for i, img_data in enumerate(image_data):
        base, ext = os.path.splitext(img_data['file'])
        category_prefix = categories[img_data['category']]
        filename = f"{i:03d}_{img_data['gradient_value']:.3f}_{category_prefix}_{base}{ext}"
        shutil.copy2(img_data['path'], os.path.join(gradient_folder, filename))

    print("\nCategory summary:")
    for category, count in categories_count.items():
        print(f"{category}: {count} images")

    with open(os.path.join(destination_folder, "gradient_info.txt"), 'w') as f:
        f.write("Image gradients (0–1):\n\n")
        for i, img_data in enumerate(image_data):
            f.write(f"{i:03d}: {img_data['gradient_value']:.3f} - {img_data['category']} - {img_data['file']}\n")

if __name__ == "__main__":
    print("Starting analysis and image sorting...")
    analyze_and_sort_images()
    print("\nDone! Sorted images are saved in folder:\n" + gradient_folder)
