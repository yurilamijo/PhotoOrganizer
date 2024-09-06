import os
import datetime

FORMAT_DATE_TIME = "%Y-%m-%d_%H-%M-%S"

def create_directory_if_needed(base_path: str, file_path: str) -> None:
    """
    This function checks if a directory for the year and month of a file's creation timestamp exists.
    If the directory does not exist, it creates the directory.

    Parameters:
    file_path (str): The absolute or relative path to the file.

    Returns:
    None: This function does not return any value. It prints a success message if the directory is created, or an error message if the directory already exists.
    """
    file_created_datetime = get_file_creation_datetime(file_path)
    file_created_datetime_year_string = str(file_created_datetime.year)
    file_created_datetime_month_string = get_month_in_dutch_format(file_created_datetime.month)
    directory_path_year = os.path.join(base_path, file_created_datetime_year_string)

    if does_directory_exist(base_path, file_created_datetime_year_string):
        if does_directory_exist(directory_path_year, file_created_datetime_month_string):
            None
        else:
            create_directory(directory_path_year, file_created_datetime_month_string)
    else:
        create_directory(base_path, file_created_datetime_year_string)
        create_directory(directory_path_year, file_created_datetime_month_string)

def get_month_in_dutch_format(month_number: int) -> str:
    """
    Converts a given month number into its Dutch equivalent.

    Parameters:
    month_number (int): The number of the month (1-12).

    Returns:
    str: The Dutch equivalent of the given month number.

    Raises:
    ValueError: If the month_number is not within the range of 1-12.
    """
    match month_number:
        case 1:
            return "januari"
        case 2:
            return "februari"
        case 3:
            return "maart"
        case 4:
            return "april"
        case 5:
            return "mei"
        case 6:
            return "juni"
        case 7:
            return "juli"
        case 8:
            return "augustus"
        case 9:
            return "september"
        case 10:
            return "oktober"
        case 11:
            return "november"
        case 12:
            return "december"
        case _:
            raise ValueError(f"Invalid month number: {month_number}")

def get_file_creation_datetime(file_path: str) -> datetime.datetime:
    """
    Retrieves the creation timestamp of a file located at the specified file path.

    Parameters:
    file_path (str): The absolute or relative path to the file.

    Returns:
    datetime.datetime: The creation timestamp of the file. The timestamp is converted to a datetime object.
    """
    file_timestamp = os.path.getctime(file_path)

    return datetime.datetime.fromtimestamp(file_timestamp)

def does_directory_exist(directory_path: str, directory_name: str) -> bool:
    """
    Check if a directory with the given name exists in the specified video directory.

    Parameters:
    directory_name (str): The name of the directory to check.

    Returns:
    bool: True if the directory exists, False otherwise.
    """
    directory_path = os.path.join(directory_path, directory_name)

    return os.path.exists(directory_path)

def create_directory(directory_path: str, directory_name: str) -> None:
    """
    Creates a new directory with the given name in the specified video directory.

    Parameters:
    directory_name (str): The name of the directory to create. The name should not contain any special characters or spaces.

    Returns:
    None: This function does not return any value. It prints a success message if the directory is created, or an error message if the directory already exists.
    """
    new_directory_path = os.path.join(directory_path, directory_name)
    print(f"create: {new_directory_path}")

    if not os.path.exists(new_directory_path):
        os.makedirs(new_directory_path)
        print(f"Directory '{directory_name}' created successfully.")
    else:
        print(f"Directory '{directory_name}' already exists.")
