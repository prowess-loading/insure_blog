import sys
from setup.browser_setup import BrowserSetup
from pages.homepage import HomePage
from pages.other_visits import OtherVisits
from pages.insurance_details import InsuranceDetails
import random
from setup import utils
from setup.ad_clicker import AdClicker


class MainExecutor:
    def __init__(
            self, device_type="both",
            proxy_active=True,
            device_name="random",
            browser_name="random",
            region="us",
            add_utm=False,
            visit_other_sites=False,
            enable_ad_click=True,
            ad_click_frequency=1
    ):
        self.device_type = device_type
        self.proxy_active = proxy_active
        self.device_name = device_name
        self.browser_name = browser_name
        self.region = region
        self.add_utm = add_utm
        self.visit_other_sites = visit_other_sites
        self.enable_ad_click = enable_ad_click
        self.ad_click_frequency = ad_click_frequency

    def get_num_tests(self):
        if len(sys.argv) > 2:
            try:
                num_tests = int(sys.argv[1])
                if num_tests <= 0:
                    print("The number of tests should be greater than 0.")
                    return None
                if num_tests > 1000:
                    print("The maximum number of tests allowed is 1000.")
                    return None
                return num_tests
            except ValueError:
                print("Please provide a valid number for <num_tests>.")
                return None
        else:
            try:
                num_tests = int(
                    input("How many times do you want to run the test? (Max: 1000): ")
                )
                if num_tests <= 0:
                    print("The number of tests should be greater than 0.")
                    return None
                if num_tests > 1000:
                    print("The maximum number of tests allowed is 1000.")
                    return None
                return num_tests
            except ValueError:
                print("Please enter a valid number.")
                return None

    def setup_driver(self):
        browser_setup = BrowserSetup()
        return browser_setup.setup_browser(
            self.device_type,
            self.proxy_active,
            device_name=self.device_name,
            browser_name=self.browser_name,
            region=self.region,
        )

    def process_run(self, driver, click_ad, ad_log_file, device_type):

        if self.visit_other_sites:
            other_visits = OtherVisits(driver)
            other_visits.process_urls_with_navigation()

        target_url = utils.target_url(self.add_utm)
        utils.open_url_with_retry(driver, target_url)

        homepage = HomePage(driver)
        insurance_page = InsuranceDetails(
            driver, homepage.selected_insurance_name)
        ad_clicker = AdClicker(driver)

        if click_ad:
            random_target = random.choice(["homepage", "insurance_page"])
            if random_target == "homepage":
                print("Clicking on ad in Homepage...")
                ad_clicker.select_random_ad(ad_log_file, device_type)
            else:
                homepage.open_insurance_page()
                print("Clicking on ad in Insurance Page...")
                ad_clicker.select_random_ad(ad_log_file, device_type)
        else:
            homepage.open_insurance_page()
            insurance_page.scroll_insurance_details_page()
