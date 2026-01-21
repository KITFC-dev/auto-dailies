import random
import re

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from src.locators import wait_for, find
from src.logger import prinfo, prwarn, prerror, prsuccess
from src.common import random_sleep, get_swal, scroll_into
from src.config import CONFIG
from src.models import Case, CasesResult
from src.constants import BASE_URL, IGNORE_CASES, \
    CaseSelectors, Condition

def get_cases(driver) -> list[Case]:
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    if driver.current_url != BASE_URL:
        driver.get(BASE_URL)

    try:
        # Get cases box's elements in a container
        container = wait_for(Condition.PRESENCE, wait, CaseSelectors.BOX)
        cases = find(container, CaseSelectors.CASE, multiple=True)
        res: list[Case] = []

        # Parse the data
        for case in cases:
            # Link
            href = case.get_attribute("href")
            if not href:
                continue

            img = find(case, CaseSelectors.IMAGE)
            name = find(case, CaseSelectors.NAME)
            price = find(case, CaseSelectors.PRICE)

            res.append(
                Case(
                    link=href,
                    image=img.get_attribute("src") if img else None,
                    name=name.text if name else None,
                    price=price.text if price else None,
                    is_ignored=href.split("/")[-1] in IGNORE_CASES
                )
            )

        return res
    except TimeoutException:
        prwarn("Couldn't find cases box element.")

    return []

def open_case(driver, case_link) -> bool:
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    if driver.current_url != case_link:
        driver.get(case_link)

    try:
        wait_for(Condition.PRESENCE, wait, CaseSelectors.CARD_LIST)
        # Wait for card animation to finish
        random_sleep(3)
        
        # Extract requirements for the case
        case_price = None
        reqs_el = find(driver, CaseSelectors.REQUIREMENTS)
        if reqs_el:
            # Find all elements that have requirement text
            req_els = find(reqs_el, CaseSelectors.REQUIREMENT, multiple=True)
            for req_el in req_els:
                text = req_el.text.strip()
                if 'чайник' in text.lower():
                    match = re.search(r'\d+', text)
                    if match:
                        case_price = int(match.group())
                        if case_price > CONFIG.case_price_threshold:
                            prinfo(f"Case price ({case_price}) is higher than threshold ({CONFIG.case_price_threshold}), skipping...")
                            return False

        if case_price is None:
            prinfo("No coin requirement found, opening the case anyway...")
        else:
            prinfo(f"Case price: {case_price} coins. Opening...")

        card_el = find(driver, CaseSelectors.CARD_LIST)
        if card_el:
            available_cards = find(card_el, CaseSelectors.CARD, multiple=True)
            picked_card = random.choice(available_cards)
            scroll_into(driver, picked_card)
            picked_card.click()

            if not get_swal(driver).text:
                return True
    except TimeoutException:
        prwarn(f"Couldn't find the case with link {case_link}.")

    return False

def run_cases(driver) -> CasesResult:
    opened_cases = 0
    ignored_cases = 0

    try:
        available_cases = get_cases(driver)
        for case in available_cases:
            # Skip ignored cases
            if not case.is_ignored:
                prinfo(f"Opening case: {case.name}")
                if open_case(driver, case.link):
                    prsuccess(f"Opened case: {case.name}")
                    opened_cases += 1
                else:
                    prerror(f"Failed to open case: {case.name}")
                        
                # Cooldown after each case
                random_sleep(7)
            else:
                ignored_cases += 1

        return CasesResult(
            success=True,
            available_cases=available_cases,
            opened_cases=opened_cases,
            ignored_cases=ignored_cases,
        )
    except Exception as e:
        prerror(f"Cases action failed: {e}")
        return CasesResult(success=False, reason=str(e))
