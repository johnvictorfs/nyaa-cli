from colorama import Fore

import logging


class CustomFormatter(logging.Formatter):
    """
    https://stackoverflow.com/a/56944256/10416161
    Logging Formatter to add colors and count warning / errors
    """

    log_format = "%(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: Fore.LIGHTWHITE_EX + log_format + Fore.RESET,
        logging.INFO: Fore.LIGHTWHITE_EX + log_format + Fore.RESET,
        logging.WARNING: Fore.YELLOW + log_format + Fore.RESET,
        logging.ERROR: Fore.RED + log_format + Fore.RESET,
        logging.CRITICAL: Fore.RED + log_format + Fore.RESET
    }

    def format(self, record: logging.LogRecord):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)

        return formatter.format(record)

