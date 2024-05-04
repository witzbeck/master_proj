#!/bin/bash

# Threshold size in bytes (10 MB)
threshold_size=$((10 * 1024 * 1024))

# Loop through all PDF files in the current directory and subdirectories
find . -name '*.pdf' -type f | while read file; do
    # Get file size
    file_size=$(stat -c "%s" "$file")

    # Check if the file size is greater than the threshold
    if [ "$file_size" -ge "$threshold_size" ]; then
        # Track this file with Git LFS
        git lfs track "$file"
        echo "$file tracked with Git LFS"
    else
        echo "$file not tracked with Git LFS"
    fi
done

# Add the .gitattributes file to the repo
git add .gitattributes
