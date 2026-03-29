#!/bin/bash
set -x
mkdir -p public/images
while read fname; do
  echo "Downloading $fname ..."
  curl -v -fSL "https://caliweedkaufen.de/images/$fname" -o "public/images/$fname"
done < images.txt
echo "All images downloaded to public/images/"