import time
from setup.main_executor import MainExecutor
from setup import utils
import random


def main():
    executor = MainExecutor()
    num_tests = executor.get_num_tests()
    if num_tests is None:
        return

    for i in range(1, num_tests + 1):
        start_time = time.time()
        print(f"\nRunning test #{i}...\n")
        driver = None

        click_ad = utils.should_click_ad(
            i, interval=executor.ad_click_frequency) if executor.enable_ad_click else False

        if executor.device_type == "both":
            executor.device_type = random.choice(["desk", "mobile"])

        try:
            driver = executor.setup_driver()
            executor.process_run(driver, click_ad)

        finally:
            if driver:
                driver.quit()
            print(f"Test #{i} completed in {time.time() - start_time:.2f}s.")


if __name__ == "__main__":
    main()
