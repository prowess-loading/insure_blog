import random
from selenium.webdriver.common.by import By
import time
from setup.smooth_scroll import SmoothScroll
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class AdClicker:
    def __init__(self, driver):
        self.driver = driver

    def get_primary_ads(self):
        elements = self.driver.find_elements(
            By.CSS_SELECTOR, "div[class^='code-block code-block-']")

        primary_visible_ads = []

        for element in elements:
            height = self.driver.execute_script(
                "return arguments[0].offsetHeight;", element)

            if height > 0:
                class_name = element.get_attribute('class')
                css_selector = f".{class_name.replace(' ', '.')}"
                primary_visible_ads.append(css_selector)

        return primary_visible_ads

    def get_side_ads(self):
        asides = self.driver.find_elements(
            By.CSS_SELECTOR, "#right-sidebar aside")

        side_ads = []
        for aside in asides:
            id_attribute = aside.get_attribute('id')
            class_attribute = aside.get_attribute('class')

            if id_attribute and id_attribute.startswith('block-') and 'widget_search' not in class_attribute:
                css_selector = f"aside#{id_attribute} > div"
                side_ads.append(css_selector)

        return side_ads

    def select_random_ad(self):
        smooth_scroll = SmoothScroll(self.driver)

        primary_visible_ads = self.get_primary_ads()
        side_ads = self.get_side_ads()
        # all_ads = primary_visible_ads + side_ads
        all_ads = side_ads

        if all_ads:
            selected_ad = random.choice(all_ads)
            print(f"Selected ad: {selected_ad}")

            smooth_scroll.scroll_to_single(selected_ad)

            random_timeout = random.randint(5, 20)
            print(
                f"Waiting for {random_timeout} seconds before quitting the driver.")

            time.sleep(random_timeout)
            self.driver.quit()

        else:
            print("No visible elements found with height > 0.")
            return None
