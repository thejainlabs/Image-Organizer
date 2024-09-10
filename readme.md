Sure! Here’s a `README.md` file that you can use for documenting your code:

---

# Image Organizer Script

## Overview

This Python script organizes images and videos from multiple source directories into a structured destination directory. The organization is based on the creation date of the files, and duplicates are handled by moving them to a separate folder. Files that cannot be processed are also moved to a designated folder for review.

## Features

- **Organizes Images and Videos**: Sorts files into year and month-based folders.
- **Handles Duplicates**: Moves duplicate images to a `duplicates` folder with `_a` and `_b` suffixes.
- **Processes Non-Media Files**: Moves non-image/video files into a `non-media` folder, with subfolders for documents and archives.
- **Handles Unrecognizable Files**: Moves files with unrecognized data streams to an `unrecognized_files` folder.
- **Logging**: Detailed logs of actions taken, including errors encountered.

## Requirements

- Python 3.x
- Pillow library (`PIL`): Install using `pip install pillow`

## Usage

1. **Update Paths**:
   - Edit the `source_directories` list to include paths to your source directories.
   - Set the `destination_directory` to the path where you want the organized files to be saved.

2. **Run the Script**:
   - Execute the script from the command line or your preferred Python environment.

```bash
python tidy_image_folder.py
```

## Script Details

### `create_folder_structure(base_dir, year=None, month=None)`

Creates the folder structure based on the year and month. If no date is available, creates an `unknown_date` folder.

### `get_image_date(image_path)`

Attempts to retrieve the creation date from the image’s EXIF data. Falls back to file modification time if EXIF data is unavailable.

### `move_file(src, dest)`

Moves a file from the source path to the destination path, creating necessary directories.

### `organize_images(source_dirs, dest_dir)`

Main function that:
- Iterates through source directories.
- Processes each file to determine its type and date.
- Moves files to appropriate folders.
- Handles duplicates and unrecognized files.

## Folder Structure in Destination Directory

- **`duplicates/`**: Contains duplicate images with `_a` and `_b` suffixes.
- **`non-media/`**:
  - **`documents/`**: Contains documents (e.g., PDFs, DOCs).
  - **`archives/`**: Contains archived files (e.g., ZIP, RAR).
  - **`misc/`**: Contains other non-media files.
- **`unrecognized_files/`**: Contains files that could not be processed.

## Error Handling

- Files with unrecognized data streams or unsupported formats are moved to `unrecognized_files/`.
- Duplicates are moved to the `duplicates/` folder.

## Example

```python
source_directories = [r'D:\pics_dump1', r'D:\pics_dump2']
destination_directory = r'D:\Organized_Pictures'

organize_images(source_directories, destination_directory)
```

## License

This script is provided as-is. Feel free to modify it to suit your needs.

---

Feel free to adjust any section or add more details as needed!