import os
import difflib

IMAGES_TXT = "images.txt"
IMAGES_DIR = "public/images"

with open(IMAGES_TXT) as f:
    desired = [line.strip() for line in f if line.strip()]

def get_downloaded():
    return set(os.listdir(IMAGES_DIR))

for want in desired:
    downloaded = get_downloaded()
    if want in downloaded:
        print(f"{want} already exists, skipping.")
        continue
    matches = difflib.get_close_matches(want, downloaded, n=1, cutoff=0.3)
    if matches:
        src = os.path.join(IMAGES_DIR, matches[0])
        dst = os.path.join(IMAGES_DIR, want)
        try:
            print(f"Renaming {matches[0]} -> {want}")
            os.rename(src, dst)
        except FileNotFoundError:
            print(f"File {matches[0]} not found, skipping.")
    else:
        print(f"No match found for {want}")

print("Done renaming. Reload your site to check product images.")