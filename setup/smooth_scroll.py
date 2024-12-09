import random
import time
from setup import utils
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class SmoothScroll:
    def __init__(self, driver, speed=50.0):
        self.driver = driver
        self.speed = speed

    def _scroll(self, scroll_amount, total_scroll_height):
        current_position = self.driver.execute_script(
            "return window.pageYOffset;")
        next_position = min(
            max(0, current_position + scroll_amount), total_scroll_height)
        scroll_step = int(scroll_amount / abs(scroll_amount) * self.speed)

        for position in range(int(current_position), int(next_position), int(scroll_step)):
            self.driver.execute_script(
                f"window.scrollTo(0, {min(position, total_scroll_height)});")
            time.sleep(0.03 + random.uniform(-0.03, 0.03))

        return self.driver.execute_script("return window.pageYOffset;")

    def _toggle_scroll_direction(self, scrolling_up, toggle_up_once):
        if not scrolling_up and random.random() < 0.1 and not toggle_up_once:
            return True, True
        elif scrolling_up:
            return False, toggle_up_once
        return scrolling_up, toggle_up_once

    def _random_pause(self):
        if random.random() < 0.015:
            time.sleep(1 + random.uniform(0, 1))
        else:
            time.sleep(random.uniform(0.3, 0.6))

    def wait_for_element(driver, timeout=10):
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                print(
                    f"Timeout reached: Could not find the target element within {timeout} seconds.")
                driver.quit()
                return False

    def scroll_to_single(self, target_selector, by=By.CSS_SELECTOR):
        try:
            target_element = self.driver.find_element(by, target_selector)
        except NoSuchElementException:
            print(f"Element with selector '{target_selector}' not found.")
            return

        scrolling_up = False
        toggle_up_once = False

        while True:
            target_in_view = self.driver.execute_script(
                "var rect = arguments[0].getBoundingClientRect();"
                "return (rect.top >= 0 && rect.bottom <= window.innerHeight);",
                target_element,
            )
            if target_in_view:
                time.sleep(3)
                try:
                    target_element.click()
                except Exception as e:
                    print(
                        f"Error: Element is not clickable or another issue occurred: {e}")
                break

            scroll_amount = - \
                random.randint(
                    80, 150) if scrolling_up else random.randint(300, 700)
            self._scroll(scroll_amount, self.driver.execute_script(
                "return document.body.scrollHeight"))

            scrolling_up, toggle_up_once = self._toggle_scroll_direction(
                scrolling_up, toggle_up_once)
            self._random_pause()

    def scroll_to_end(self):
        max_attempts = 4
        attempts = 0
        scrolling_up = False
        toggle_up_once = False
        total_scroll_height = self.driver.execute_script(
            "return document.body.scrollHeight")

        early_quit_threshold = random.uniform(
            0.3, 0.5) * total_scroll_height if random.random() < 0.4 else None

        while True:
            current_position = self.driver.execute_script(
                "return window.pageYOffset")
            total_scroll_height = self.driver.execute_script(
                "return document.body.scrollHeight")

            scroll_amount = - \
                random.randint(
                    80, 150) if scrolling_up else random.randint(400, 800)
            new_position = self._scroll(scroll_amount, total_scroll_height)

            if early_quit_threshold and new_position >= early_quit_threshold:
                print(f"Early quitting...")
                self.driver.quit()
                break

            if new_position == current_position:
                attempts += 1
                if attempts >= max_attempts:
                    print("Scrolling stagnated. Exiting...")
                    break
            else:
                attempts = 0

            scrolling_up, toggle_up_once = self._toggle_scroll_direction(
                scrolling_up, toggle_up_once)
            self._random_pause()

            if new_position >= total_scroll_height - 1:
                print("Reached the end of the page.")
                break

    def scroll_and_navigate(self, next_url):
        max_attempts = 4
        attempts = 0
        scrolling_up = False
        toggle_up_once = False
        total_scroll_height = self.driver.execute_script(
            "return document.body.scrollHeight")

        early_quit_threshold = random.uniform(
            0.6, 0.8) * total_scroll_height if random.random() < 0.6 else None

        while True:
            current_position = self.driver.execute_script(
                "return window.pageYOffset")
            total_scroll_height = self.driver.execute_script(
                "return document.body.scrollHeight")

            scroll_amount = - \
                random.randint(
                    80, 250) if scrolling_up else random.randint(200, 500)
            new_position = self._scroll(scroll_amount, total_scroll_height)

            if early_quit_threshold and new_position >= early_quit_threshold:
                print(f"Early quitting... Navigating to {next_url}")
                utils.open_url_with_retry(self.driver, next_url)
                return

            if new_position == current_position:
                attempts += 1
                if attempts >= max_attempts:
                    print("Scrolling stagnated. Navigating to the next URL...")
                    utils.open_url_with_retry(self.driver, next_url)
                    return
            else:
                attempts = 0

            scrolling_up, toggle_up_once = self._toggle_scroll_direction(
                scrolling_up, toggle_up_once)
            self._random_pause()

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

        scrolling_up = False
        toggle_up_once = False
        start_time = time.time()
        timeout = 15

        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                print(
                    f"Timeout reached: Could not find the target ad within {timeout} seconds.")
                self.driver.quit()
                break

            target_in_view = self.driver.execute_script(
                "var rect = arguments[0].getBoundingClientRect();"
                "return (rect.top >= 0 && rect.bottom <= window.innerHeight);",
                target_element,
            )
            if target_in_view:
                try:
                    time.sleep(2)
                    target_element.click()
                    print("ad Clicked")
                    switch_to_new_tab(self.driver)
                    print(f"Will sleep for {quit_time} seconds")
                    time.sleep(quit_time)
                    utils.increment_ad_click_count(log_file)
                    self.driver.quit()
                except (Exception) as e:
                    print(
                        f"Error: Element is not clickable or another issue occurred: {e}")
                break

            scroll_amount = - \
                random.randint(
                    80, 150) if scrolling_up else random.randint(200, 500)
            self._scroll(scroll_amount, self.driver.execute_script(
                "return document.body.scrollHeight"))

            scrolling_up, toggle_up_once = self._toggle_scroll_direction(
                scrolling_up, toggle_up_once)
            self._random_pause()


def switch_to_new_tab(driver):
    driver.switch_to.window(driver.window_handles[-1])
