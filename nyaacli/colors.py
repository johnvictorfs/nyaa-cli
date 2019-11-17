from inquirer.themes import Theme
from blessings import Terminal
from colorama import init

init()


def red(text: str) -> str:
    return f'\033[31m{text}\033[0m'


def green(text: str) -> str:
    return f'\33[92m{text}\033[0m'


def yellow(text: str) -> str:
    return f'\33[33m{text}\033[0m'


def blue(text: str) -> str:
    return f'\33[34m{text}\033[0m'


class PromptTheme(Theme):
    def __init__(self):
        super(PromptTheme, self).__init__()

        term = Terminal()

        self.Question.mark_color = term.yellow
        self.Question.brackets_color = term.normal
        self.Question.default_color = term.normal
        self.Editor.opening_prompt_color = term.bright_black
        self.Checkbox.selection_color = term.blue
        self.Checkbox.selection_icon = '❯'
        self.Checkbox.selected_icon = '◉'
        self.Checkbox.selected_color = term.yellow + term.bold
        self.Checkbox.unselected_color = term.normal
        self.Checkbox.unselected_icon = '◯'
        self.List.selection_color = term.blue
        self.List.selection_cursor = '❯'
        self.List.unselected_color = term.normal
