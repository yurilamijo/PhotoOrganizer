import os
import shutil
import concurrent.futures

def move_files_to_destination_directories(source_directory: str, destination_directory_photos: str, destination_directory_videos: str) -> None:
    """
    This function moves files from a source directory to separate destination directories based on their file types.

    Parameters:
    source_directory (str): The path of the source directory where the files are located.
    destination_directory_photos (str): The path of the destination directory for image files.
    destination_directory_videos (str): The path of the destination directory for video files.

    Returns:
    None: The function does not return any value. It moves the files to the respective destination directories.
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

    for root, dirs, files in os.walk(source_directory):
        for file in files:
            path_file = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1].lower()

            if file_extension in file_extension_map:
                destination_directory = file_extension_map[file_extension]
                shutil.move(path_file, destination_directory)
                print(f"Moved file: '{file}' from path: '{path_file}' to destination: '{destination_directory}'")
            else:
                print(f"Invalid file extension found: {file_extension} in path: '{path_file}'")

def copy_files_to_destination_directories(source_directory: str, destination_directory_photos: str, destination_directory_videos: str) -> None:
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

    with concurrent.futures.ThreadPoolExecutor() as executor:
        batches = []

        for root, dirs, files in os.walk(source_directory):
            for file in files:
                path_file = os.path.join(root, file)
                file_extension = os.path.splitext(file)[1].lower()

                if file_extension in file_extension_map:
                    destination_directory = file_extension_map[file_extension]
                    batches.append((path_file, destination_directory))

                    if len(batches) >= batch_size:
                        executor.submit(move_batch_of_files, batches)
                        batches = []
                else:
                    print(f"Invalid file extension found: {file_extension} in path: '{path_file}'")
        
        if batches:
            executor.submit(move_batch_of_files, batches)

def move_batch_of_files(batches: list) -> None:
    for source_path, destination_directory in batches:
        try:
            shutil.move(source_path, destination_directory)
            print(f"Moved file: '{os.path.basename(source_path)}' from path: '{source_path}' to destination: '{destination_directory}'")
        except Exception as e:
            print(f"Error moved file: '{os.path.basename(source_path)}' from path: '{source_path}' to destination: '{destination_directory}': {str(e)}")