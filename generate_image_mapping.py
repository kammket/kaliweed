import os
import difflib
import json

IMAGES_TXT = "images.txt"
IMAGES_DIR = "public/images"
MAPPING_FILE = "image_mapping_suggestions.json"

with open(IMAGES_TXT) as f:
    desired = [line.strip() for line in f if line.strip()]

actual = os.listdir(IMAGES_DIR)

mapping = {}
for want in desired:
    matches = difflib.get_close_matches(want, actual, n=3, cutoff=0.2)
    mapping[want] = matches

with open(MAPPING_FILE, "w") as f:
    json.dump(mapping, f, indent=2)

print(f"Mapping suggestions written to {MAPPING_FILE}. Review and use for manual or automated updates.")
