import time
import random

from pathlib import Path

def random_sleep(amount: float = 2.0, r: float = 0.5):
    """Sleep for certain amount of time with a random jitter. """
    time.sleep(max(0.0, amount + random.uniform(-r, r)))

def diff_text(label: str, init_val: int, curr_val: int) -> str:
    """Generates a diff stylized text from id. """
    if init_val < curr_val:
        diff = '+'
    elif init_val > curr_val:
        diff = '-'
    else:
        diff = ' '

    return f"{diff} {label.title()}: {init_val} -> {curr_val}\n"

def is_docker():
    """Check if running in a Docker container. """
    cgroup = Path('/proc/self/cgroup')
    return Path('/.dockerenv').is_file() or (cgroup.is_file() and 'docker' in cgroup.read_text())
