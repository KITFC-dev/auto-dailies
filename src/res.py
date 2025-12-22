import os
import sys

from config import CHROMIUM_PATH, CHROMEDRIVER_PATH

FILES = {}

def f(rp):
    bp = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(bp, rp)

def load_resources():
    global FILES
    chromium_path = f(CHROMIUM_PATH)
    for file in os.listdir(chromium_path):
        FILES[f"chromium/{file}"] = os.path.join(chromium_path, file)

    FILES["chromedriver.exe"] = f(CHROMEDRIVER_PATH)

def get_chromium_binary():
    return FILES.get(CHROMIUM_PATH)

def get_chromedriver():
    return FILES.get(CHROMEDRIVER_PATH)
