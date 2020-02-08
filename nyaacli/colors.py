from prompt_toolkit import styles
from colorama import init, Fore, Style

init()


def red(text: str) -> str:
    return Fore.RED + text + Style.RESET_ALL


def green(text: str) -> str:
    return Fore.GREEN + text + Style.RESET_ALL


def yellow(text: str) -> str:
    return Fore.YELLOW + text + Style.RESET_ALL


def blue(text: str) -> str:
    return Fore.BLUE + text + Style.RESET_ALL


prompt_style = styles.Style([
    ('qmark', 'fg:#5F819D bold'),
    ('question', 'fg:#289c64 bold'),
    ('answer', 'fg:#48b5b5 bold'),
    ('pointer', 'fg:#48b5b5 bold'),
    ('highlighted', 'fg:#07d1e8'),
    ('selected', 'fg:#48b5b5 bold'),
    ('separator', 'fg:#6C6C6C'),
    ('instruction', 'fg:#77a371'),
    ('text', ''),
    ('disabled', 'fg:#858585 italic')
])
