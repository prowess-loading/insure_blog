import sys
import time
from setup.browser_setup import BrowserSetup
from pages.homepage import HomePage
from pages.other_visits import OtherVisits
from pages.insurance_details import InsuranceDetails
import random
from setup import utils
from selenium.common.exceptions import TimeoutException


def main():

    if len(sys.argv) > 1:
        try:
            num_tests = int(sys.argv[1])
            if num_tests <= 0:
                print("The number of tests should be greater than 0.")
                return
            if num_tests > 1000:
                print("The maximum number of tests allowed is 1000.")
                return
        except ValueError:
            print("Please provide a valid number for <num_tests>.")
            return
    else:
        try:
            num_tests = int(
                input("How many times do you want to run the test? (Max: 1000): "))
            if num_tests <= 0:
                print("The number of tests should be greater than 0.")
                return
            if num_tests > 1000:
                print("The maximum number of tests allowed is 1000.")
                return
        except ValueError:
            print("Please enter a valid number.")
            return

    device_type = "desk"        # desk, mobile
    proxy_active = True         # True, False
    add_utm = False             # True, False
    visit_other_sites = True    # True, False

    # Execute tests
    for i in range(1, num_tests + 1):
        start_time = time.time()
        print(f"\nRunning test #{i}...\n")
        driver = None

        if device_type == "both":
            device_type = random.choice(["desk", "mobile"])

        try:
            browser_setup = BrowserSetup()
            driver = browser_setup.setup_browser(
                device_type,
                proxy_active,
                device_name="random",       # random
                browser_name="random",      # random, chrome, firefox, edge, safari
                region="us"                 # rd, us, na, au, as, eu
            )

            if visit_other_sites:
                other_visits = OtherVisits(driver)
                other_visits.process_urls_with_navigation()

            target_url = utils.target_url(add_utm)

            try:
                driver.get(target_url)
            except TimeoutException:
                print("Network timeout occurred, refreshing the page...")

            homepage = HomePage(driver)
            insurance_page = InsuranceDetails(
                driver, homepage.selected_insurance_name)

            homepage.open_insurance_page()
            insurance_page.scroll_insurance_details_page()

        finally:
            if driver:
                driver.quit()
            print(f"Test #{i} completed in {time.time() - start_time:.2f}s.")


if __name__ == "__main__":
    main()
