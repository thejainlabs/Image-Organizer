import os
import shutil
from datetime import datetime
from PIL import Image, UnidentifiedImageError
import filecmp

def create_folder_structure(base_dir, year=None, month=None):
    """Create the folder structure based on year and month, or 'unknown_date' if no date is available."""
    if year and month:
        year_folder = os.path.join(base_dir, str(year))
        month_folder = os.path.join(year_folder, f"{year}_{month}")
    else:
        # Folder for files with unknown date
        month_folder = os.path.join(base_dir, 'unknown_date')

    os.makedirs(month_folder, exist_ok=True)
    return month_folder

def get_image_date(image_path):
    """Try to get the creation date of an image or fallback to file's modification time."""
    try:
        # Only attempt to read EXIF data for image files
        if image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.heif')):
            image = Image.open(image_path)
            exif_data = image.getexif()
            if exif_data and 36867 in exif_data:  # EXIF DateTimeOriginal tag
                date_str = exif_data[36867]
                return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
    except UnidentifiedImageError:
        raise UnidentifiedImageError(f"Cannot identify image file: {image_path}")
    except Exception as e:
        raise Exception(f"Error reading EXIF data from {image_path}: {e}")

    # Fallback to file's modification time
    return datetime.fromtimestamp(os.path.getmtime(image_path))

def move_file(src, dest):
    """Move file to the destination, creating directories as needed."""
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.move(src, dest)

def organize_images(source_dirs, dest_dir):
    """Organize images from multiple source directories into the destination."""
    log_file = os.path.join(dest_dir, 'organize_log.txt')
    duplicate_dir = os.path.join(dest_dir, 'duplicates')
    non_media_dir = os.path.join(dest_dir, 'non-media')
    unrecognized_dir = os.path.join(dest_dir, 'unrecognized_files')
    
    os.makedirs(duplicate_dir, exist_ok=True)
    os.makedirs(non_media_dir, exist_ok=True)
    os.makedirs(unrecognized_dir, exist_ok=True)

    duplicate_count = 1

    with open(log_file, 'w', encoding='utf-8') as log:
        for src_dir in source_dirs:
            for root, _, files in os.walk(src_dir):
                for file in files:
                    file_path = os.path.join(root, file)

                    # Skip unsupported or corrupted files
                    if not file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.mp4', '.avi', '.mov', '.heif')):
                        ext = file.split('.')[-1].lower()
                        if ext in ['pdf', 'doc', 'docx', 'txt']:
                            file_type_dir = os.path.join(non_media_dir, 'documents')
                        elif ext in ['zip', 'rar']:
                            file_type_dir = os.path.join(non_media_dir, 'archives')
                        else:
                            file_type_dir = os.path.join(non_media_dir, 'misc')

                        move_file(file_path, os.path.join(file_type_dir, file))
                        log.write(f"Moved non-media file: {file_path} to {file_type_dir}\n")
                        continue

                    try:
                        # Get creation date of the image or video
                        image_date = get_image_date(file_path)
                        if image_date is None:
                            log.write(f"Could not determine date for {file_path}, moving to 'unknown_date' folder.\n")
                            dest_folder = create_folder_structure(dest_dir)  # Create 'unknown_date' folder
                        else:
                            year = image_date.year
                            month = image_date.month
                            dest_folder = create_folder_structure(dest_dir, year, month)

                        # Prepare destination path
                        dest_path = os.path.join(dest_folder, file)

                        # Handle duplicates
                        if os.path.exists(dest_path) and filecmp.cmp(file_path, dest_path, shallow=False):
                            duplicate_a = os.path.join(duplicate_dir, f"{duplicate_count}_a{os.path.splitext(file)[-1]}")
                            duplicate_b = os.path.join(duplicate_dir, f"{duplicate_count}_b{os.path.splitext(file)[-1]}")
                            move_file(file_path, duplicate_a)
                            shutil.copy2(dest_path, duplicate_b)  # Copy the original duplicate
                            duplicate_count += 1
                            log.write(f"Duplicate detected: {file_path} and {dest_path}, moved to {duplicate_a} and {duplicate_b}\n")
                        else:
                            move_file(file_path, dest_path)
                            log.write(f"Moved {file_path} to {dest_path}\n")
                    
                    except (UnidentifiedImageError, Exception) as e:
                        unrecognized_path = os.path.join(unrecognized_dir, file)
                        move_file(file_path, unrecognized_path)
                        log.write(f"Error processing file {file_path}. Moved to 'unrecognized_files': {unrecognized_path}. Error: {e}\n")

    print(f"Organization complete. Log file saved at: {log_file}")

# Example usage for multiple source directories
source_directories = [r'D:\pics_dump', r'D:\OneDrive\dump\pics\pics dump\pics dump\dump']
destination_directory = r'D:\Organized_Pictures'

organize_images(source_directories, destination_directory)
