import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.logger import prinfo, prwarn
from config import ELEMENTS, BASE_URL

def get_cases(driver):
    wait = WebDriverWait(driver, 2)
    driver.get(BASE_URL)

    try:
        # Wait until cases box is present
        container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, ELEMENTS["case_box"])))

        # Get cases box's elements
        cases_elements = container.find_elements(By.CLASS_NAME, ELEMENTS["case"])
        cases_data = []

        # Parse the data
        for case in cases_elements:
            link = case.get_attribute("href")
            img = case.find_element(By.CLASS_NAME, ELEMENTS["case_image"]).get_attribute("src")
            name = case.find_element(By.CLASS_NAME, ELEMENTS["case_name"]).text
            price = case.find_element(By.CLASS_NAME, ELEMENTS["case_price"]).text

            cases_data.append({
                "name": name,
                "price": price,
                "link": link,
                "image": img
            })

        return cases_data
    except Exception:
        prwarn("Couldn't find cases box element.")

def get_case_info(driver, case_link):
    # Will be implemented later
    pass

def open_case(driver):
    # Will be implemented later
    pass
