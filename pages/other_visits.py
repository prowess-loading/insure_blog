import random
from setup.smooth_scroll import SmoothScroll
from data import website_visit
from setup import utils


class OtherVisits:

    def __init__(self, driver):
        self.driver = driver

    def process_urls_with_navigation(self):

        url_list = website_visit.university_sites
        selected_urls = random.sample(url_list, min(
            random.choice([2, 3]), len(url_list)))

        smooth_scroll = SmoothScroll(self.driver)

        for i, url in enumerate(selected_urls):
            print(f"Processing URL {i+1}/{len(selected_urls)}: {url}")
            utils.open_url_with_retry(self.driver, url)

            next_url = selected_urls[i + 1] if i + \
                1 < len(selected_urls) else None

            if next_url:
                smooth_scroll.scroll_and_navigate(next_url)
