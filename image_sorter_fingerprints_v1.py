from pathlib import Path
import os
import cv2
import numpy as np
import shutil
from sklearn.decomposition import PCA
from tqdm import tqdm

def create_color_fingerprint(image, fingerprint_size=64):
    # Convert to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Calculate HSV histogram
    hist = cv2.calcHist([hsv], [0, 1, 2], None, [8, 8, 1], [0, 180, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()

    # Pad or truncate to the desired fingerprint size
    if len(hist) < fingerprint_size:
        hist = np.pad(hist, (0, fingerprint_size - len(hist)))
    elif len(hist) > fingerprint_size:
        hist = hist[:fingerprint_size]
    
    return hist

def analyze_images_in_folder(folder_path):
    fingerprints = []
    filenames = []

    print("Scanning folder:", folder_path)
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"Found {len(image_files)} images to analyze.")
    print("Analyzing images and computing color fingerprints...")

    for idx, filename in enumerate(tqdm(image_files)):
        filepath = os.path.join(folder_path, filename)
        image = cv2.imread(filepath)
        if image is None:
            print(f"Cannot read file: {filename}")
            continue
        fingerprint = create_color_fingerprint(image)
        fingerprints.append(fingerprint)
        filenames.append(filename)

    return np.array(fingerprints), filenames

def sort_and_save_images(fingerprints, filenames, source_folder, output_folder):
    # Use PCA for dimensionality reduction
    pca = PCA(n_components=1)
    projections = pca.fit_transform(fingerprints).flatten()
    
    # Sort based on the first principal component
    sorted_indices = np.argsort(projections)
    os.makedirs(output_folder, exist_ok=True)

    print("Copying files to output folder in sorted order...")

    for idx, i in enumerate(sorted_indices):
        src_path = os.path.join(source_folder, filenames[i])
        dst_filename = f"{(idx + 1) * 100:06d}_{filenames[i]}"
        dst_path = os.path.join(output_folder, dst_filename)
        shutil.copy2(src_path, dst_path)

    print("Finished copying and sorting images.")

# Paths (automatically resolved relative to script location)
base_dir = Path(__file__).resolve().parent
source_folder = base_dir / "photo_source"  # Folder with images to sort
output_folder = source_folder / "FINGERPRINTsorted"  # Output folder for sorted images

# Execute
fingerprints, filenames = analyze_images_in_folder(source_folder)
sort_and_save_images(fingerprints, filenames, source_folder, output_folder)
