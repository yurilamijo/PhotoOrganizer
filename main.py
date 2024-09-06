import os

import directory_generator

PATH_BASE = "/Volumes/T7 Shield"
DIRECTORY_PHOTOS = "/Photos"
DIRECTORY_VIDEOS = "/Videos"
PATH_DIRECTORY_PHOTOS = PATH_BASE + DIRECTORY_PHOTOS
PATH_DIRECTORY_VIDEOS = PATH_BASE + DIRECTORY_VIDEOS

def get_all_directories_and_files() -> None:
    """
    This function retrieves all directories and files within the specified video directory.
    It prints the names of the directories and files along with their creation timestamps.

    Parameters:
    None

    Returns:
    None
    """
    # Get all directories in the Photos directory
    dir_list = os.listdir(PATH_DIRECTORY_VIDEOS)
    print(f"All Directories and Files in '{PATH_DIRECTORY_VIDEOS}'")

    # Print all directories and files
    for file in dir_list:
        file_path = os.path.join(PATH_DIRECTORY_VIDEOS, file)

        if os.path.isfile(file_path):
            directory_generator.create_directory_if_needed(PATH_DIRECTORY_VIDEOS, file_path)

            print(f"File: {file}")
        elif os.path.isdir(file_path):
            print(f"Directory: {file}")
        else:
            print(f"Unknown file type: {file}")

get_all_directories_and_files()