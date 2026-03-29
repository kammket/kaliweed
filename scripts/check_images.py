import os
from PIL import Image
import json

# Path to images and products data
IMAGES_DIR = os.path.join(os.path.dirname(__file__), '../public/images')
PRODUCTS_PATH = os.path.join(os.path.dirname(__file__), '../src/data/products.ts')

# Helper to extract product image paths from products.ts

def extract_product_images(products_path):
    images = []
    with open(products_path, encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line.startswith('image: '):
            # e.g. image: "/images/alien-labs-zangria.webp",
            img = line.split('image: ')[1].split(',')[0].strip().strip('"\'')
            if img.startswith('/images/'):
                images.append(img[8:])  # remove leading '/images/'
    return images

def get_image_size(image_path):
    try:
        with Image.open(image_path) as img:
            return img.size
    except Exception:
        return None

def main():
    product_images = extract_product_images(PRODUCTS_PATH)
    files = set(os.listdir(IMAGES_DIR))
    missing = []
    blurry = []
    for img in product_images:
        if img not in files:
            missing.append(img)
        else:
            size = get_image_size(os.path.join(IMAGES_DIR, img))
            if size and (size[0] < 500 or size[1] < 500):
                blurry.append({'file': img, 'size': size})
    print('Missing images:')
    for m in missing:
        print('  ', m)
    print('\nPotentially blurry images (less than 500x500):')
    for b in blurry:
        print(f"  {b['file']} - {b['size']}")
    # Save results for further automation
    with open('missing_images.json', 'w') as f:
        json.dump({'missing': missing, 'blurry': blurry}, f, indent=2)

if __name__ == '__main__':
    main()
