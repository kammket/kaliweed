# This script generates placeholder images for all missing product images referenced in products.ts.
# It uses Pillow to create a simple placeholder with the product/image name.

import os
import re
from PIL import Image, ImageDraw, ImageFont

PRODUCTS_TS = "../src/data/products.ts"
IMAGES_DIR = "../public/images/"
PLACEHOLDER_SIZE = (600, 600)
BG_COLOR = (240, 240, 240)
TEXT_COLOR = (80, 80, 80)
FONT_SIZE = 32

# Extract all referenced image filenames from products.ts
image_pattern = re.compile(r'image: "/images/([^"]+)"')

with open(PRODUCTS_TS, "r", encoding="utf-8") as f:
    products_ts = f.read()

referenced_images = set(image_pattern.findall(products_ts))

# List all files in the images directory
available_images = set(os.listdir(IMAGES_DIR))

missing_images = sorted([img for img in referenced_images if img not in available_images])

# Try to use a default font
try:
    font = ImageFont.truetype("arial.ttf", FONT_SIZE)
except:
    font = ImageFont.load_default()

for img_name in missing_images:
    img = Image.new("RGB", PLACEHOLDER_SIZE, BG_COLOR)
    draw = ImageDraw.Draw(img)
    text = os.path.splitext(img_name)[0].replace('-', ' ').replace('_', ' ')
    # Use textbbox for Pillow >=8.0.0
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except AttributeError:
        w, h = font.getsize(text)
    draw.text(((PLACEHOLDER_SIZE[0]-w)//2, (PLACEHOLDER_SIZE[1]-h)//2), text, fill=TEXT_COLOR, font=font)
    img.save(os.path.join(IMAGES_DIR, img_name))
    print(f"Created placeholder: {img_name}")

print("All missing images now have placeholders.")
