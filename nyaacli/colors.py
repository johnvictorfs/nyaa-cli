from PyInquirer import Token, style_from_dict
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


prompt_style = style_from_dict({
    Token.Separator: '#6C6C6C',
    Token.QuestionMark: '#5F819D',
    Token.Selected: '#48b5b5 bold',
    Token.Pointer: '#48b5b5 bold',
    Token.Instruction: '#77a371',
    Token.Answer: '#48b5b5 bold',
    Token.Question: '#289c64 bold',
})
