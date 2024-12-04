import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from data.agents_data import desk_agents
from data.utms import main_page, utms
from data.agents_data import ios_versions, apple_crios_versions, apple_fxios_versions, apple_edgios_versions


def target_url(add_utm):
    if add_utm:
        base_url = random.choice(main_page)
        utm_param = random.choice(utms)

        return f"{base_url}{utm_param}"
    else:
        return random.choice(main_page)


def open_url_with_retry(driver, url, max_retries=3, retry_delay=5):
    for attempt in range(max_retries):
        try:
            driver.get(url)

            # Check if the page contains "502 Bad Gateway"
            if "502 Bad Gateway" in driver.page_source:
                print(
                    f"502 error detected. Retrying... ({attempt + 1}/{max_retries})")
                sleep(retry_delay)  # Wait before retrying
                continue
            break
        except TimeoutException:
            print(
                f"Timeout occurred. Retrying... ({attempt + 1}/{max_retries})")
            sleep(retry_delay)
    else:
        print("Failed to load the page after multiple attempts.")


def get_mobile_user_agent(device, browser_name):

    if device["deviceMetrics"]["isiOS"]:
        if browser_name == "chrome":
            browser_ios_name = "CriOS"
            browser_version = random.choice(apple_crios_versions)
        elif browser_name == "firefox":
            browser_ios_name = "Fxios"
            browser_version = random.choice(apple_fxios_versions)
        elif browser_name == "edge":
            browser_ios_name = "Edgios"
            browser_version = random.choice(apple_edgios_versions)

        ios_version = random.choice(ios_versions)
        user_agent = f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_version} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) {browser_ios_name}/{browser_version} Mobile/15E148 Safari/604.1"

    else:
        android_version = random.choice(range(9, 15))
        chrome_version = random.choice(apple_crios_versions)
        model = device["deviceMetrics"]["model"]
        user_agent = f"Mozilla/5.0 (Linux; Android {android_version}; {model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Mobile Safari/537.36"

    return user_agent


def get_desk_user_agent():
    return random.choice(desk_agents)


def adjust_dimensions(device, browser_deltas, browser_name):
    delta = browser_deltas.get(browser_name, {"width": 0, "height": 0})
    width = round((device["deviceMetrics"]["width"] +
                  delta["width"]) / device["deviceMetrics"]["pixelRatio"])
    height = round((device["deviceMetrics"]["height"] +
                   delta["height"]) / device["deviceMetrics"]["pixelRatio"])
    return width, height


def set_window_size(driver, device, browser_deltas, browser_name):
    width, height = adjust_dimensions(device, browser_deltas, browser_name)
    driver.set_window_size(width, height)


def random_wait():
    sec = random.randint(1, 3)
    sleep(sec)


def should_click_ad(test_index, interval):
    interval_start = ((test_index - 1) // interval) * interval + 1
    interval_end = interval_start + interval - 1
    return test_index == random.randint(interval_start, interval_end)


def fill_input(driver, locator, value):

    element = driver.find_element(By.CSS_SELECTOR, locator)
    driver.execute_script(
        "arguments[0].setAttribute('type', 'text');", element)

    if element.is_displayed() and element.is_enabled():
        element.clear()
        element.send_keys(str(value))
        sleep(0.5)
        return
    else:
        raise ElementNotInteractableException(
            "Element not interactable.")
