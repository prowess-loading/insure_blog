import time
import sys
from setup.main_executor import MainExecutor
from setup import utils
import random


def main():
    num_tests = int(sys.argv[1])
    terminal_number = int(sys.argv[2])
    ad_click_log_file = sys.argv[3]
    terminal_log_file = sys.argv[4]

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

            # Start the process in a loop to monitor time
            while True:
                elapsed_time = time.time() - start_time
                if elapsed_time > 120:
                    print(
                        f"Test #{i}: Exceeded 120 seconds. Quitting driver...")
                    driver.quit()
                    break

                executor.process_run(driver, click_ad)
                break

            executor.process_run(driver, click_ad, ad_click_log_file)

        finally:
            if driver:
                driver.quit()

            duration = time.time() - start_time
            print(
                f"Terminal {terminal_number}: Test #{i} completed in {duration:.2f}s.")
            utils.log_to_file(terminal_number, i, duration, terminal_log_file)


if __name__ == "__main__":
    main()
