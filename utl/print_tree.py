import os
import sys

# Force UTF-8 encoding to handle special characters
sys.stdout.reconfigure(encoding='utf-8')

def print_tree(directory, prefix=""):
    """Recursively prints directory tree structure."""
    try:
        entries = sorted(os.listdir(directory))  # Sort for consistency
        for i, entry in enumerate(entries):
            path = os.path.join(directory, entry)
            is_last = (i == len(entries) - 1)
            connector = "└── " if is_last else "├── "
            print(prefix + connector + entry)
            if os.path.isdir(path):
                extension = "    " if is_last else "│   "
                print_tree(path, prefix + extension)
    except PermissionError:
        print(prefix + "└── [Access Denied]")

# Get the path of the script and set project root
script_dir = os.path.dirname(os.path.abspath(__file__))  # Get directory of the script
project_root = os.path.dirname(script_dir)  # One level above the script directory

print_tree(project_root)
