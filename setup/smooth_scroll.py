import random
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from setup.Commenter import Commenter


class SmoothScroll:
    def __init__(self, driver, speed=20.0):

        self.driver = driver
        self.speed = speed

    def _execute_smooth_scroll(self, current_position, next_position, scroll_step):
        for position in range(current_position, next_position, scroll_step):
            self.driver.execute_script(
                f"window.scrollTo(0, {max(0, position)});")
            time.sleep(random.uniform(0.02, 0.05))  # Mimic smooth scrolling

    def _calculate_next_position(self, current_position, target_position, scrolling_up):
        scroll_amount = (-random.randint(80, 200)
                         if scrolling_up else random.randint(200, 500))
        next_position = current_position + scroll_amount

        if (scrolling_up and next_position <= target_position) or (not scrolling_up and next_position >= target_position):
            next_position = target_position

        return next_position, scroll_amount

    def _scroll_to_target(self, target_position, current_position, scrolling_up):
        while current_position != target_position:
            next_position, scroll_amount = self._calculate_next_position(
                current_position, target_position, scrolling_up
            )
            scroll_step = int(scroll_amount / abs(scroll_amount) * self.speed)
            self._execute_smooth_scroll(
                current_position, next_position, scroll_step)
            current_position = next_position

            # Mimic human-like pauses
            time.sleep(random.uniform(0.3, 0.6) if random.random()
                       >= 0.02 else random.uniform(1, 3))

            # Occasionally toggle direction
            if not scrolling_up and random.random() < 0.1:
                scrolling_up = True
            elif scrolling_up and random.random() < 0.1:
                scrolling_up = False

            yield current_position

    def scroll(self, target_selector=None, scroll_to_end=False, by=By.CSS_SELECTOR):

        total_scroll_height = self.driver.execute_script(
            "return document.body.scrollHeight")
        current_position = self.driver.execute_script(
            "return window.pageYOffset;")
        scrolling_up = False

        early_quit_threshold = random.uniform(
            0.6, 0.8) * total_scroll_height if random.random() < 0.2 else None

        while True:
            if target_selector:
                try:
                    print(f"Scrolling to target: {target_selector}")
                    target_element = self.driver.find_element(
                        by, target_selector)
                    target_in_view = self.driver.execute_script(
                        "var rect = arguments[0].getBoundingClientRect();"
                        "return (rect.top >= 0 && rect.bottom <= window.innerHeight);",
                        target_element,
                    )
                    if target_in_view:
                        time.sleep(2)
                        target_element.click()
                        break
                except NoSuchElementException:
                    pass

            for current_position in self._scroll_to_target(
                total_scroll_height if scroll_to_end else current_position,
                current_position,
                scrolling_up,
            ):
                if scroll_to_end:
                    if early_quit_threshold and current_position >= early_quit_threshold:
                        print(f"Early quitting...")
                        self.driver.quit()
                        return

                    if current_position >= total_scroll_height:

                        if random.random() < 0.1:
                            print("Adding comment...")
                            comment = Commenter(self.driver)
                            comment.enter_comment()
                            time.sleep(2)

                        print("Reached the end of the page, quitting...")
                        self.driver.quit()
                        return

    def scroll_to_end_and_close(self):
        print("Scrolling to the end of the page...")
        self.scroll(scroll_to_end=True)
