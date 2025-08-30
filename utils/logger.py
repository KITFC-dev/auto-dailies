from colorama import Fore, Style

def prinfo(msg): print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {msg}")
def prsuccess(msg): print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {msg}")
def prwarn(msg): print(f"{Fore.YELLOW}[WARN]{Style.RESET_ALL} {msg}")
def prerror(msg): print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {msg}")
