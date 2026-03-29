import os
import json

IMAGES_DIR = "public/images"
MAPPING_FILE = "image_mapping_suggestions.json"

with open(MAPPING_FILE) as f:
    mapping = json.load(f)

renamed = set()
for want, matches in mapping.items():
    for match in matches:
        src = os.path.join(IMAGES_DIR, match)
        dst = os.path.join(IMAGES_DIR, want)
        if os.path.exists(src) and not os.path.exists(dst) and match not in renamed:
            print(f"Renaming {match} -> {want}")
            os.rename(src, dst)
            renamed.add(match)
            break

print("Done. Reload your site to check product images.")
