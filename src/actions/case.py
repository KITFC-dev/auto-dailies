import random

from selenium.webdriver.support.ui import WebDriverWait

from src.logger import prinfo, prerror, prsuccess, prdebug
from src.config import CONFIG
from src.models import Case, CasesResult
from src.common import random_sleep, get_swal, parse_num, click_el, \
    handle_exceptions, wait_for, find
from src.constants import BASE_URL, IGNORE_CASES, \
    CaseSelectors, Condition

def get_cases(driver) -> list[Case]:
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    if driver.current_url != BASE_URL:
        driver.get(BASE_URL)

    # Get case elements
    container = wait_for(Condition.PRESENCE, wait, CaseSelectors.BOX)
    cases = find(container, CaseSelectors.CASE, multiple=True)
    res: list[Case] = []

    # Parse data
    for case in cases:
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
                is_ignored=href.split("/")[-1] in IGNORE_CASES,
                is_target=href.split("/")[-1].lower() == CONFIG.target_case.lower(),
            )
        )

    return res

def open_case(driver, case: Case) -> bool:
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    if driver.current_url != case.link:
        driver.get(case.link)

    wait_for(Condition.PRESENCE, wait, CaseSelectors.CARD_LIST)
    random_sleep(3) # card animation
    
    # Extract case price
    case_price = None
    reqs_el = find(driver, CaseSelectors.REQUIREMENTS)
    if reqs_el:
        # Find all elements that have requirement text
        req_els = find(reqs_el, CaseSelectors.REQUIREMENT, multiple=True)
        for req_el in req_els:
            text = req_el.text.strip()
            if 'чайник' in text.lower():
                case_price = parse_num(text)

    # Decide if to open the case
    if case.is_target:
        prinfo("Target case detected. Opening regardless of price...")
    elif case_price is None:
        prinfo("No coin requirement found, opening the case anyway...")
    elif case_price > CONFIG.case_price_threshold:
        prinfo(f"Case price ({case_price}) is higher than threshold ({CONFIG.case_price_threshold}), skipping...")
        return False
    else:
        prinfo(f"Case price: {case_price} coins. Opening...")

    # Open the case
    card_el = find(driver, CaseSelectors.CARD_LIST)
    if card_el:
        available_cards = find(card_el, CaseSelectors.CARD, multiple=True)
        click_el(driver, random.choice(available_cards))

        # Check if successful
        swal = get_swal(driver)
        if not swal.text:
            return True

    return False

@handle_exceptions(default=CasesResult(success=False, reason="Failed to open cases"))
def run_cases(driver) -> CasesResult:
    opened_cases = 0
    ignored_cases = 0
    available_cases = get_cases(driver)

    for case in available_cases:
        # Skip ignored cases, unless target
        if case.is_target or not case.is_ignored:
            prinfo(f"Opening case: {case.name}")
            if open_case(driver, case):
                prsuccess(f"Opened case: {case.name}")
                opened_cases += 1
            else:
                prerror(f"Failed to open case: {case.name}")
                        
            # Cooldown after each case
            random_sleep(7)
        else:
            ignored_cases += 1

    data = CasesResult(
        success=True,
        available_cases=available_cases,
        opened_cases=opened_cases,
        ignored_cases=ignored_cases,
    )
    prdebug(f"Cases result: {data}")
    return data
