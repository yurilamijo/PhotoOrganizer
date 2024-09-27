import os
import shutil

import directory_generator
import directory_file_transfer_helper

PATH_BASE = "/Volumes/T7 Shield"
PATH_BASE_NO_NAME = "/Volumes/NO NAME"
DIRECTORY_PHOTOS = "/photos"
DIRECTORY_VIDEOS = "/videos"
PATH_DIRECTORY_PHOTOS = PATH_BASE + DIRECTORY_PHOTOS
PATH_DIRECTORY_VIDEOS = PATH_BASE + DIRECTORY_VIDEOS

def execute() -> None:
    sort_files_by_creation_date()
    # move_files_to_destination_directories()

def sort_files_by_creation_date() -> None:
    sort_all_directories_and_files(PATH_DIRECTORY_VIDEOS)
    sort_all_directories_and_files(PATH_DIRECTORY_PHOTOS)

def move_files_to_destination_directories() -> None:
    directory_file_transfer_helper.execute(PATH_BASE_NO_NAME, PATH_DIRECTORY_PHOTOS, PATH_DIRECTORY_VIDEOS)

def sort_all_directories_and_files(path_base: str) -> None:
    """
    This function iterates through all files and directories within a given base directory.
    For each file, it creates a directory if needed and moves the file to the appropriate destination directory based on its creation date.
    For each directory, it simply prints its name.
    If an unknown file type is encountered, it prints the file's name and path.

    Parameters:
    path_base (str): The base directory path where the function will start searching for files and directories.

    Returns:
    None: The function does not return any value. It prints messages indicating the file and directory operations.
    """
    for file in os.listdir(path_base):
        path_file = os.path.join(path_base, file)

        if os.path.isfile(path_file):
            directory_generator.create_directory_if_needed(path_base, path_file)
            move_file_to_destination_directory(path_base, path_file, file)

        elif os.path.isdir(path_file):
            print(f"Directory: {file}")
        else:
            print(f"Unknown file type: {file} with path: {path_file}")

def move_file_to_destination_directory(path_base: str, path_file: str, file: str) -> None:
    """
    This function moves a file from its current location to a destination directory based on the file's creation date.

    Parameters:
    path_base (str): The base directory path where the destination directory will be created.
    path_file (str): The full path of the file to be moved.
    file (str): The name of the file to be placed in the destination directory.

    Returns:
    None: The function does not return any value. It prints a message indicating the file's movement.
    """
    file_created_datetime = directory_generator.get_file_creation_datetime(path_file)
    file_created_datetime_year_string = str(file_created_datetime.year)
    file_created_datetime_month_string = directory_generator.get_month_in_dutch_format(file_created_datetime.month)
    destination_directory = determine_destination_directory_based_on_year_and_month(path_base, file_created_datetime_year_string, file_created_datetime_month_string, file)

    shutil.move(path_file, destination_directory)
    print(f"File Moved from: {path_file} to {destination_directory}")

def determine_destination_directory_based_on_year_and_month(path_base: str, year: str, month: str, file: str) -> str:
    """
    This function constructs the destination directory path based on the provided year, month, and file name.

    Parameters:
    path_base (str): The base directory path where the destination directory will be created.
    year (str): The year as a string.
    month (str): The month as a string.
    file (str): The name of the file to be placed in the destination directory.

    Returns:
    str: The constructed destination directory path.
    """
    return os.path.join(path_base, year, month, file)

if __name__ == "__main__":
    execute()