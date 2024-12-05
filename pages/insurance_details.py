import json
import random
import time
from selenium.webdriver.common.by import By
from setup.smooth_scroll import SmoothScroll
from setup import utils


class InsuranceDetails:

    def __init__(self, driver, selected_insurance):
        self.driver = driver
        self.selected_insurance = selected_insurance

        with open('data/page_locators.json', 'r') as f:
            self.locators = json.load(f)

    def scroll_insurance_details_page(self):
        navigator = SmoothScroll(self.driver)

        if random.random() < 0.4:

            prev_btn = self.locators["insurance_page"]["prev"]
            next_btn = self.locators["insurance_page"]["next"]
            selected_btn = random.choice([prev_btn, next_btn])

            insurance_name = self.driver.find_element(
                By.CSS_SELECTOR, selected_btn).text
            print(f"Selected another Insurance: {insurance_name}")

            navigator.scroll_to_single(selected_btn)
            time.sleep(3)
            navigator.scroll_to_end()
            utils.ensure_browser_quit(self.driver)

        else:
            navigator.scroll_to_end()
            utils.ensure_browser_quit(self.driver)
