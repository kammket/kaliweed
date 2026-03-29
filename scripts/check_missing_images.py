# This script checks which product images referenced in products.ts are missing from the /public/images/ directory.
# It outputs a list of missing images for manual review or further automation.

import os
import re

PRODUCTS_TS = "../src/data/products.ts"
IMAGES_DIR = "../public/images/"

# Extract all referenced image filenames from products.ts
image_pattern = re.compile(r'image: "/images/([^"]+)"')

with open(PRODUCTS_TS, "r", encoding="utf-8") as f:
    products_ts = f.read()

referenced_images = set(image_pattern.findall(products_ts))

# List all files in the images directory
available_images = set(os.listdir(IMAGES_DIR))

missing_images = sorted([img for img in referenced_images if img not in available_images])

if missing_images:
    print("Missing images (referenced in products.ts but not found in /public/images/):")
    for img in missing_images:
        print(img)
else:
    print("All referenced images are present in /public/images/.")
