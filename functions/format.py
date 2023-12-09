from colorama import init, Fore, Back, Style
def format_text(text, color=Fore.WHITE, background=None, style=None):
    formatted_text = f"{color}{background}{style}{text}{Style.RESET_ALL}"
    return formatted_text