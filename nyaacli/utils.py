import os
import subprocess
import platform


def clear_screen():
    """
    Runs either 'cls' or 'clear' on the Terminal, 'cls' to clear Terminal on windows,
    which will ignore the rest of the command, and 'clear' to clear on Linux/Mac OS
    """
    os.system('cls||clear')


def xdg_open(file_path: str):
    """
    Open file with default for that file-format, or a program selection otherwise
    """
    if platform.system() == 'Darwin':
        # MacOS
        subprocess.call(('open', file_path))
    elif platform.system() == 'Windows':
        # Windows
        windows_path = os.path.abspath(file_path)

        os.system(f'start #{windows_path}')
    else:
        # Linux
        subprocess.call(('xdg-open', file_path))
