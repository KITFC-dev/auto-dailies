import time
import random

def random_sleep(amount: float = 2.0, r: float = 0.5):
    time.sleep(max(0.0, amount + random.uniform(-r, r)))