import time
import os
import shutil
import concurrent.futures

def execute(source_directory: str, destination_directory_photos: str, destination_directory_videos: str) -> None:
    start_time = time.time()
    move_files_to_destination_directories(source_directory, destination_directory_photos, destination_directory_videos)
    end_time = time.time()
    print(f"Execution Time: {end_time - start_time} seconds")

def move_files_to_destination_directories(source_directory: str, destination_directory_photos: str, destination_directory_videos: str) -> None:
    """
    This function moves files from a source directory to specific destination directories based on their file extensions.
    It uses a ThreadPoolExecutor to process multiple files concurrently.

    Parameters:
    source_directory (str): The path of the source directory where the files are located.
    destination_directory_photos (str): The path of the destination directory for photos.
    destination_directory_videos (str): The path of the destination directory for videos.

    Returns:
    None
    """
    file_extension_map = {
        ".jpg": destination_directory_photos,
        ".jpeg": destination_directory_photos,
        ".png": destination_directory_photos,
        ".mov": destination_directory_videos,
        ".mp4": destination_directory_videos,
        ".avi": destination_directory_videos,
        ".mkv": destination_directory_videos,
        ".mpg": destination_directory_videos,
    }

    batch_size = 100

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        batches = []

        for root, dirs, files in os.walk(source_directory):
            for file in files:
                path_file = os.path.join(root, file)
                file_extension = os.path.splitext(file)[1].lower()

                if file_extension in file_extension_map:
                    destination_directory = file_extension_map[file_extension]

                    if should_move_file(path_file, destination_directory):
                        batches.append((path_file, destination_directory))

                    if len(batches) >= batch_size:
                        executor.submit(move_batch_of_files, batches.copy())
                        batches.clear()
                else:
                    print(f"Invalid file extension found: {file_extension} in path: '{path_file}'")

        if batches:
            executor.submit(move_batch_of_files, batches)

def move_batch_of_files(batches: list) -> None:
    """
    This function moves a batch of files from their source paths to their respective destination directories.

    Parameters:
    batches (list): A list of tuples, where each tuple contains the source path (str) and the destination directory (str) of a file.

    Returns:
    None

    The function iterates over the provided batches and attempts to move each file to its designated destination directory.
    If a file is successfully moved, it prints a success message.
    If an error occurs during the file movement, it prints an error message with the details of the exception.
    """
    for source_path, destination_directory in batches:
        try:
            if not os.path.exists(destination_directory):
                os.makedirs(destination_directory)
                
            shutil.move(source_path, destination_directory)
            print(f"Moved file: '{os.path.basename(source_path)}' to destination: '{destination_directory}'")
        except Exception as e:
            print(f"Error moving file: '{os.path.basename(source_path)}' from '{source_path}' to '{destination_directory}': {str(e)}")

def should_move_file(source_directory: str, destination_directory: str) -> bool:
    """
    This function determines whether a file should be moved from its source directory to its designated destination directory.

    Parameters:
    source_directory (str): The path of the source directory where the file is located.
    destination_directory (str): The path of the destination directory for the file.

    Returns:
    bool: True if the file should be moved, False otherwise.

    The function checks if the destination directory already contains a file with the same name as the source file.
    If it does, the function returns False, indicating that the file should not be moved.
    Otherwise, it returns True, indicating that the file should be moved.
    """
    file_name = os.path.basename(source_directory)
    destination_file_path = os.path.join(destination_directory, file_name)

    return not os.path.exists(destination_file_path)