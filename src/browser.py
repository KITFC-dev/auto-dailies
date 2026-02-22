import pickle
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from src.config import CONFIG
from src.common import is_docker

def create_driver():
    options = webdriver.ChromeOptions()
    options.binary_location = CONFIG.chromium_path
    if (CONFIG.headless if not CONFIG.new_account else False):
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
    if is_docker():
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    service = Service(executable_path=CONFIG.chromedriver_path)
    return webdriver.Chrome(service=service, options=options)

def load_cookies(driver, cookie_file) -> tuple[bool, str]:
    """
    Load cookies and injects them to the driver,
    also capitalizes "sameSite" cookie attribute
    as some browsers may raise an error.

    Returns:
        tuple[bool, str]: (success, error)
    """
    if os.path.exists(cookie_file):
        try:
            cookies = pickle.load(open(cookie_file, "rb"))
            for cookie in cookies:
                if 'sameSite' in cookie:
                    cookie['sameSite'] = cookie['sameSite'].capitalize()
                driver.add_cookie(cookie)
            return True, ""
        except Exception as e:
            return False, f"Failed to load cookies: {e}"
    return False, "Cookie file not found."

def save_cookies(driver, cookie_file): pickle.dump(driver.get_cookies(), open(cookie_file, "wb"))
