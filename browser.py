from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def create_driver(chrome_binary, chromedriver_path, headless=False):
    options = webdriver.ChromeOptions()
    options.binary_location = chrome_binary
    if headless:
        options.add_argument("--headless")

    service = Service(executable_path=chromedriver_path)
    return webdriver.Chrome(service=service, options=options)
