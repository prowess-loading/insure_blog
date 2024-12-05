import random
from time import sleep
from setup import utils
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class SmoothScroll:
    def __init__(self, driver, speed=50.0):
        self.driver = driver
        self.speed = speed

    def scroll_to_single(self, target_selector, by=By.CSS_SELECTOR):
        try:
            target_element = self.driver.find_element(by, target_selector)
        except NoSuchElementException:
            print(f"Element with selector '{target_selector}' not found.")
            return

        current_position = self.driver.execute_script(
            "return window.pageYOffset;")
        scrolling_up = False
        toggle_up_once = False

        while True:
            target_in_view = self.driver.execute_script(
                "var rect = arguments[0].getBoundingClientRect();"
                "return (rect.top >= 0 && rect.bottom <= window.innerHeight);",
                target_element,
            )
            if target_in_view:
                sleep(3)
                try:
                    target_element.click()
                except Exception as e:
                    print(
                        f"Error: Element is not clickable or another issue occurred: {e}")
                break

            # Adjust scroll amount based on direction
            scroll_amount = (
                -random.randint(80, 150) if scrolling_up else random.randint(300, 700)
            )
            next_position = int(current_position) + scroll_amount

            # Smooth scroll in small steps
            scroll_step = int(scroll_amount / abs(scroll_amount) * self.speed)
            for position in range(int(current_position), next_position, scroll_step):
                self.driver.execute_script(
                    f"window.scrollTo(0, {max(0, position)});"
                )
                sleep(0.02)

            current_position = next_position

            # Toggle scrolling direction occasionally
            if not scrolling_up and random.random() < 0.1 and not toggle_up_once:
                scrolling_up = True
                toggle_up_once = True
            elif scrolling_up:
                scrolling_up = False

            if random.random() < 0.015:
                sleep(1)
            else:
                sleep(random.uniform(0.3, 0.6))

    def scroll_to_end(self):
        max_attempts = 4
        attempts = 0
        scrolling_up = False
        toggle_up_once = False
        total_scroll_height = self.driver.execute_script(
            "return document.body.scrollHeight")

        early_quit_threshold = random.uniform(
            0.3, 0.5) * total_scroll_height if random.random() < 0.3 else None

        while True:
            current_position = self.driver.execute_script(
                "return window.pageYOffset")
            total_scroll_height = self.driver.execute_script(
                "return document.body.scrollHeight")

            scroll_amount = (
                -random.randint(80, 150) if scrolling_up else random.randint(300, 700)
            )
            next_position = min(
                max(0, current_position + scroll_amount), total_scroll_height)

            # Perform smooth scrolling
            scroll_step = int(scroll_amount / abs(scroll_amount) * self.speed)

            for position in range(int(current_position), int(next_position), int(scroll_step)):

                self.driver.execute_script(
                    f"window.scrollTo(0, {min(position, total_scroll_height)});"
                )
                sleep(0.03 + random.uniform(-0.03, 0.03))

            new_position = self.driver.execute_script(
                "return window.pageYOffset")

            if early_quit_threshold and new_position >= early_quit_threshold:
                print(f"Early quitting...")
                self.driver.quit()
                break

            # Check if the position has stopped changing
            if new_position == current_position:
                attempts += 1
                if attempts >= max_attempts:
                    print("Scrolling stagnated. Exiting...")
                    break
            else:
                attempts = 0  # Reset attempts if movement detected

            if not scrolling_up and random.random() < 0.1 and not toggle_up_once:
                scrolling_up = True
                toggle_up_once = True
            elif scrolling_up:
                scrolling_up = False

            if random.random() < 0.015:
                sleep(1 + random.uniform(0, 1))
            else:
                sleep(random.uniform(0.3, 0.6))

            if new_position >= total_scroll_height - 1:
                print("Reached the end of the page.")
                break

    def scroll_and_navigate(self, next_url):
        max_attempts = 4
        attempts = 0
        scrolling_up = False
        toggle_up_once = False

        # Fetch total scroll height
        total_scroll_height = self.driver.execute_script(
            "return document.body.scrollHeight")

        # Early quit threshold
        early_quit_threshold = random.uniform(
            0.6, 0.8) * total_scroll_height if random.random() < 0.6 else None

        while True:
            current_position = self.driver.execute_script(
                "return window.pageYOffset")
            total_scroll_height = self.driver.execute_script(
                "return document.body.scrollHeight")

            # Randomize scrolling amount and direction
            scroll_amount = (
                -random.randint(80, 250) if scrolling_up else random.randint(200, 500)
            )
            next_position = min(
                max(0, current_position + scroll_amount), total_scroll_height)

            # Perform smooth scrolling
            scroll_step = int(scroll_amount / abs(scroll_amount) * self.speed)

            for position in range(int(current_position), int(next_position), int(scroll_step)):
                self.driver.execute_script(
                    f"window.scrollTo(0, {min(position, total_scroll_height)});")
                sleep(0.03 + random.uniform(-0.03, 0.03))

            new_position = self.driver.execute_script(
                "return window.pageYOffset")

            # Handle early quit logic
            if early_quit_threshold and new_position >= early_quit_threshold:
                print(f"Early quitting... Navigating to {next_url}")
                utils.open_url_with_retry(self.driver, next_url)
                return

            # Detect stagnation in scrolling
            if new_position == current_position:
                attempts += 1
                if attempts >= max_attempts:
                    print("Scrolling stagnated. Navigating to the next URL...")
                    utils.open_url_with_retry(self.driver, next_url)
                    return
            else:
                attempts = 0  # Reset attempts if movement detected

            # Toggle direction for a single upward scroll
            if not scrolling_up and random.random() < 0.1 and not toggle_up_once:
                scrolling_up = True
                toggle_up_once = True
            elif scrolling_up:
                scrolling_up = False

            # Random pauses for natural scrolling effect
            if random.random() < 0.015:
                sleep(1 + random.uniform(0, 1))
            else:
                sleep(random.uniform(0.3, 0.6))

            # Check if we have reached the end
            if new_position >= total_scroll_height - 1:
                print("Reached the end of the page. Navigating to the next URL...")
                utils.open_url_with_retry(self.driver, next_url)
                return

    def scroll_to_ad_click(self, target_selector, quit_time, log_file, by=By.CSS_SELECTOR):
        try:
            target_element = self.driver.find_element(by, target_selector)
        except NoSuchElementException:
            print(f"Element with selector '{target_selector}' not found.")
            return

        current_position = self.driver.execute_script(
            "return window.pageYOffset;")
        scrolling_up = False
        toggle_up_once = False

        while True:
            target_in_view = self.driver.execute_script(
                "var rect = arguments[0].getBoundingClientRect();"
                "return (rect.top >= 0 && rect.bottom <= window.innerHeight);",
                target_element,
            )
            if target_in_view:
                try:
                    sleep(2)
                    target_element.click()
                    utils.increment_ad_click_count(log_file)

                    sleep(quit_time)
                    self.driver.execute_script("window.history.back();")
                    sleep(5)
                except Exception as e:
                    print(
                        f"Error: Element is not clickable or another issue occurred: {e}")
                break

            # Adjust scroll amount based on direction
            scroll_amount = (
                -random.randint(80, 150) if scrolling_up else random.randint(200, 500)
            )
            next_position = int(current_position) + scroll_amount

            # Smooth scroll in small steps
            scroll_step = int(scroll_amount / abs(scroll_amount) * self.speed)
            for position in range(int(current_position), next_position, scroll_step):
                self.driver.execute_script(
                    f"window.scrollTo(0, {max(0, position)});"
                )
                sleep(0.02)

            current_position = next_position

            # Toggle scrolling direction occasionally
            if not scrolling_up and random.random() < 0.1 and not toggle_up_once:
                scrolling_up = True
                toggle_up_once = True
            elif scrolling_up:
                scrolling_up = False

            if random.random() < 0.015:
                sleep(1)
            else:
                sleep(random.uniform(0.3, 0.6))
