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

    def scroll_insurance_details_page(self):
        utils.scroll_to_multi_or_end(self.driver)
