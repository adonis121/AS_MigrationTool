import os
from typing import List


def write_utf8_file(file_path: str, string_list: List[str], force: bool = False) -> None:
    """
    Write UTF-8 encoded text to a file.

    :param file_path: The path to the file.
    :param string_list: A list of strings to write to the file.
    :param force: If True, overwrite the file if it exists.
    """
    # Check if the file exists
    if os.path.exists(file_path):
        if force:
            os.remove(file_path)

    # Open the file in append or write mode based on existence
    mode = 'a' if os.path.exists(file_path) else 'w'

    # Write the strings to the file with UTF-8 encoding
    with open(file_path, mode, encoding='utf-8') as file:
        file.writelines(line + '\n' for line in string_list)


# Example usage
file_path = 'example.txt'
string_list = ['Hello, world!', 'This is a test.']
force = True

write_utf8_file(file_path, string_list, force)
