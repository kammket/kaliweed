import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Base URL of the shop
BASE_URL = "https://caliweedkaufen.de/shop/"
# Output directory for images
OUTPUT_DIR = "public/images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Get all product page URLs from the shop listing
print("Fetching product listing...")
resp = requests.get(BASE_URL)
soup = BeautifulSoup(resp.text, "html.parser")
product_links = set()
for a in soup.find_all("a", href=True):
    href = a["href"]
    if "/produkt/" in href:
        product_links.add(urljoin(BASE_URL, href))

print(f"Found {len(product_links)} product pages.")

# Download images from each product page
def download_image(img_url):
    filename = os.path.basename(urlparse(img_url).path)
    out_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(out_path):
        print(f"Downloading {img_url} -> {filename}")
        r = requests.get(img_url, stream=True)
        if r.status_code == 200:
            with open(out_path, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
        else:
            print(f"Failed to download {img_url} (status {r.status_code})")
    else:
        print(f"Already exists: {filename}")

for url in product_links:
    print(f"Processing {url}")
    r = requests.get(url)
    s = BeautifulSoup(r.text, "html.parser")
    # Find all images in the product gallery
    for img in s.find_all("img"):
        src = img.get("src")
        if src and "/uploads/" in src:
            download_image(src)

print("Done. Check public/images for downloaded product images.")
