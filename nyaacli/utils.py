import os


def clear_screen():
    """
    Runs either 'cls' or 'clear' on the Terminal, 'cls' to clear Terminal on windows,
    which will ignore the rest of the command, and 'clear' to clear on Linux/Mac OS
    """
    os.system('cls||clear')


def get_file_extension(path: str) -> str:
    """
    Gets the File extension from the path to a file

    'asd.txt' -> '.txt'
    'asd' -> ''
    '/path/to/asd.mkv' -> '.mkv'
    """
    filename, extension = os.path.splitext(path)

    return extension


def text_break() -> None:
    print('-' * 10, end='\n')
