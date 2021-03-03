import sys
import typing


def check_file_type(filename: str, expected_type: typing.Union[str, list]):
    """Checks if a given file has the type or types that are passed in

    Args:
        filename (str): the filename in question
        expected_type (t.Union[str, list]): either a string with the expected
        filetype or a list of strings with expected file types
    """
    # get the extension from filename

    extension = filename.rstrip().split('.')[-1].lower()
    try:
        if type(expected_type) == str:
            # lower case both the extension and expected_type, do a string match
            assert extension == expected_type.lower()
        elif type(expected_type) == list:
            assert extension in [file_type.lower() for file_type in expected_type]
        else:
            raise ValueError(f'expected string or list but received {expected_type}')
    except AssertionError:
        sys.exit(f"The pipeline is expecting the file type to be {expected_type}, but the provided file has a file type of {extension}.")
