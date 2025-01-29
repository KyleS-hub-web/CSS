# -*- coding: utf-8 -*-
"""

"""

# Import Libraries
import os
import shutil
import pprint as pp

from certifi import where
from panel.models.perspective import theme

# Define the directory containing the messy files
dir = "messy_movie_files"

# Ensure the directory exists
if not os.path.exists(dir):
    os.makedirs(dir)

source_files = os.listdir(dir)

# Ensure the new directory exists, if not create it
new_dir = "clean_movie_files"

if not os.path.exists(new_dir):
    os.makedirs(new_dir)

# Function to normalize file names
def normalize_file_name(file_name):

    # Remove the file extension
    name, extension = os.path.splitext(file_name)

    # Replace common separators with spaces
    x = ["_", "-", ";", "!", "@", "&", ",", "."]
    for i in x:
        name = name.replace(i, " ")

    # Split into parts (words)
    name = name.split()
    # Find the year (4 digits)
    year = []
    for part in name:
        if part.isdigit() and len(part) == 4:
            year = part
            break
    else:
        return None

    
    # Get the movie title_parts (everything before the year)
    title_parts = name[:name.index(year)]

    title_parts = " ".join(title_parts)

    # Get the director (everything after the year)
    director = name[name.index(year) + 1:]

    director = " ".join(director)

    # Format the new file name
    return f"{title_parts} ({year}) - {director}{extension}"





# Process files in the source directory


    # Check old path
for file in os.listdir(dir):
    old_path = os.path.join(dir, file)
    print(file)

    if not os.path.isfile(old_path):
        continue

    # Get new file name
    new_name = normalize_file_name(file)
    print(new_name)

    # Define the new path in the new directory
    new_path = os.path.join(new_dir, new_name)

    # Copy the file to the new directory with the new name
    shutil.copy(old_path, new_path)

#%%



