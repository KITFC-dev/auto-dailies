import time
import random

from pathlib import Path

def random_sleep(amount: float = 2.0, r: float = 0.5):
    """Sleep for certain amount of time with a random jitter. """
    time.sleep(max(0.0, amount + random.uniform(-r, r)))

def is_docker():
    """Check if running in a Docker container. """
    cgroup = Path('/proc/self/cgroup')
    return Path('/.dockerenv').is_file() or (cgroup.is_file() and 'docker' in cgroup.read_text())
