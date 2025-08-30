from inputimeout import inputimeout, TimeoutOccurred
from utils.logger import prinfo

def timed_input(prompt, timeout, timeout_message="Input timed out"):
    try:
        return inputimeout(prompt=prompt, timeout=timeout)
    except TimeoutOccurred:
        prinfo(f"{timeout_message}")
        return None