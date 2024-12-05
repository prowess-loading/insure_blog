import time
import sys
from setup.main_executor import MainExecutor
from setup import utils
import random


def main():
    # Retrieve arguments
    num_tests = int(sys.argv[1])
    terminal_number = int(sys.argv[2])
    ad_click_log_file = sys.argv[3]  # Get the log file path from arguments

    executor = MainExecutor()
    for i in range(1, num_tests + 1):
        start_time = time.time()
        print(f"\nTerminal {terminal_number}: Running test #{i}...\n")
        driver = None

        click_ad = utils.should_click_ad(
            i, interval=executor.ad_click_frequency
        ) if executor.enable_ad_click else False

        if executor.device_type == "both":
            executor.device_type = random.choice(["desk", "mobile"])

        try:
            driver = executor.setup_driver()
            executor.process_run(driver, click_ad)

            # If an ad was clicked, increment the count
            if click_ad:
                utils.increment_ad_click_count(ad_click_log_file)

        finally:
            if driver:
                driver.quit()

            duration = time.time() - start_time
            print(
                f"Terminal {terminal_number}: Test #{i} completed in {duration:.2f}s.")
            utils.log_to_file(terminal_number, i, duration)


if __name__ == "__main__":
    main()
