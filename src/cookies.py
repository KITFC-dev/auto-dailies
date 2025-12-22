import pickle
import os

def load_cookies(driver, cookie_file):
    """
    Load cookies and injects them to the driver,
    also capitalizes "sameSite" cookie attribute
    as some browsers may raise an error.
    """
    if os.path.exists(cookie_file):
        cookies = pickle.load(open(cookie_file, "rb"))
        for cookie in cookies:
            if 'sameSite' in cookie:
                cookie['sameSite'] = cookie['sameSite'].capitalize()
            driver.add_cookie(cookie)
        return True
    return False

def save_cookies(driver, cookie_file): pickle.dump(driver.get_cookies(), open(cookie_file, "wb"))
