import json
import random
import time
from selenium.webdriver.common.by import By
from setup.smooth_scroll import SmoothScroll


class HomePage:
    def __init__(self, driver):
        self.driver = driver

        with open('data/page_locators.json', 'r') as f:
            self.locators = json.load(f)

        self.insurances = [
            "Travel",
            "Renters",
            "Liability",
            "Long-Term-Care",
            "Business",
            "Pet",
            "HomeOwners",
            "Life",
            "Health",
            "Auto",
        ]

        self.selected_insurance_name = random.choice(self.insurances)

    def open_insurance_page(self):
        insurance_page_article_id = self.locators["homepage"]["titles"]["articles"].get(
            self.selected_insurance_name)

        title_locator = self.locators["homepage"]["title"]
        read_more_locator = self.locators["homepage"]["read-more"]

        page_title = f"{insurance_page_article_id} {title_locator}"
        read_more = f"{insurance_page_article_id} {read_more_locator}"

        print(f"Selected Insurance: {self.selected_insurance_name}")

        selected_insurance_click_element = random.choice(
            [page_title, read_more])

        navigator = SmoothScroll(self.driver)
        navigator.scroll_to_single(selected_insurance_click_element)
