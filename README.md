📸 **Image Sorting and Visual Gradient Classifier**
This project provides a set of Python scripts for analyzing, categorizing, and sorting image collections based on visual characteristics using machine learning and heuristic rules.

It is ideal for photographers, digital artists, and content creators who wish to bring order to large collections of images by automatically assigning them into visual categories and placing them along a perceptual gradient spectrum.

🔧 **Features**
✅ Automatic image feature extraction (color histograms, brightness, saturation, entropy, edge density)

✅ Face detection for portrait classification

✅ PCA-based gradient scoring for perceptual image sorting

✅ Heuristic-based category assignment:

Vibrant

Pastel

Monochrome

Dark

Nature

Urban

Portrait

Abstract

Other

✅ Sorted export with filename prefix (position, gradient value, category)

✅ Logging and summary of results

✅ Easily configurable folder paths

📁 **Folder Structure**
bash

project/
├── image_sorting_gradient.py     # Main script
├── [your images folder]          # Input image folder
├── sortedNEWMETHOD/
│   ├── gradient/                 # Sorted images with gradient filenames
│   └── gradient_info.txt         # Detailed output with features and scores

🧠 **How it Works**
Feature Extraction: Each image is resized and analyzed to extract visual features (dominant colors, histograms, entropy, edge density, etc.).

Categorization: Images are heuristically assigned to one of several predefined visual categories.

Gradient Computation: Principal Component Analysis (PCA) is used to place each image along a single visual axis (gradient).

Sorting and Export: Images are renamed and copied in order of increasing gradient value with metadata in filename.

🚀 **Usage**
Install dependencies (if not already installed):

bash
pip install numpy opencv-python scikit-learn matplotlib pandas pillow
Adjust folder paths in the script:

python
source_folder = r"your\path\to\images"
destination_folder = r"your\output\path"
Run the script:

bash

python image_sorting_gradient.py
Sorted images will be available in sortedNEWMETHOD/gradient/ with gradient-based prefixes.

📝 Example Filename

023_0.362_04_dark_IMG1234.jpg
023: Position in gradient

0.362: Gradient score (from 0 to 1)

04_dark: Assigned category

IMG1234.jpg: Original filename

📊 Output Summary
At the end of the run, you'll get:

A console breakdown of how many images were assigned to each category.

A gradient_info.txt file listing all scores and assigned labels.

A perceptually ordered image collection ready for curation or publishing.

🧪 Scripts
This project consists of multiple versions:

Basic categorizer – sorts images into categories using heuristics.

Gradient sorter – performs PCA-based sorting using visual features.

Full version (this script) – combines categorization + gradient + output.

🤝 License
This project is licensed under the MIT License. Feel free to use, modify, and share it for personal or commercial use.
