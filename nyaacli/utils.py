import os


def clear_screen():
    """
    Runs either 'cls' or 'clear' on the Terminal, 'cls' to clear Terminal on windows,
    which will ignore the rest of the command, and 'clear' to clear on Linux/Mac OS
    """
    os.system('cls||clear')
