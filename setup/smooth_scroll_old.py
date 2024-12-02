import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class SmoothScroll:
    def __init__(self, driver, speed=20.0):
        self.driver = driver
        self.speed = speed

    def scroll(self, target_selector=None, scroll_to_end=False, by=By.CSS_SELECTOR):

        total_scroll_height = self.driver.execute_script(
            "return document.body.scrollHeight")

        current_position = self.driver.execute_script(
            "return window.pageYOffset;")

        scrolling_up = False
        toggle_up_once = False

        while True:
            final_position = total_scroll_height if scroll_to_end else current_position

            if target_selector:
                try:
                    target_element = self.driver.find_element(
                        by, target_selector)
                    target_in_view = self.driver.execute_script(
                        "var rect = arguments[0].getBoundingClientRect();"
                        "return (rect.top >= 0 && rect.bottom <= window.innerHeight);", target_element
                    )

                    if target_in_view:
                        sleep(3)
                        target_element.click()
                        break
                except NoSuchElementException:
                    pass

            # If we're scrolling up, adjust the scroll amount
            scroll_amount = - \
                random.randint(
                    80, 200) if scrolling_up else random.randint(200, 500)
            target_position = int(current_position) + scroll_amount

            scroll_step = int(scroll_amount / abs(scroll_amount) * self.speed)

            # Scroll through the page in small steps
            for position in range(int(current_position), target_position, scroll_step):
                self.driver.execute_script(
                    f"window.scrollTo(0, {max(0, position)});")
                sleep(0.02)

            current_position = target_position

            # After scrolling down, sometimes switch to scrolling up
            if not scrolling_up and random.random() < 0.1 and not toggle_up_once:
                scrolling_up = True
            elif scrolling_up:
                scrolling_up = False

            if random.random() < 0.020:
                sleep(1)
            else:
                sleep(random.uniform(0.3, 0.6))

            if scroll_to_end and current_position >= final_position:
                self.driver.quit()

    def navigate_and_scroll(self, first_target_selector, second_target_selector=None):
        if first_target_selector:
            self.scroll(first_target_selector)
            sleep(2)
        elif second_target_selector:
            print(f"Scrolling to the {second_target_selector}...")
            self.scroll(second_target_selector)
            sleep(2)
        else:
            self.scroll(scroll_to_end=True)
        print("Navigation and scrolling completed.")

    def scroll_to_single_element(self, target_selector, by=By.CSS_SELECTOR):
        target_element = self.driver.find_element(by, target_selector)
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
                target_element.click()
                break

            # Adjust scroll amount based on scrolling direction
            scroll_amount = (
                -random.randint(80,
                                200) if scrolling_up else random.randint(200, 500)
            )
            next_position = int(current_position) + scroll_amount

            # Smooth scroll in small steps
            scroll_step = int(scroll_amount / abs(scroll_amount) * self.speed)
            for position in range(int(current_position), next_position, scroll_step):
                self.driver.execute_script(
                    f"window.scrollTo(0, {max(0, position)});")
                sleep(0.02)

            current_position = next_position

            # Toggle scroll direction occasionally
            if not scrolling_up and random.random() < 0.1 and not toggle_up_once:
                scrolling_up = True
                toggle_up_once = True
            elif scrolling_up:
                scrolling_up = False

            if random.random() < 0.015:
                sleep(1)
            else:
                sleep(random.uniform(0.3, 0.6))
