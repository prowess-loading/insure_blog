import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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

            # If no error, break out of the retry loop
            print("Page loaded successfully.")
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


def select_dropdown(driver, locator, value, by=By.CSS_SELECTOR):
    dropdown = Select(driver.find_element(by, locator))

    try:
        dropdown.select_by_visible_text(value)
    except Exception:
        try:
            dropdown.select_by_value(value)
        except Exception as e:
            print(f"Failed to select '{value}' from dropdown: {e}")


def click_element(driver, locator, by=By.XPATH):
    element = driver.find_element(by, locator)
    if element.is_displayed():
        element.click()


def get_random_number(min_value, max_value):
    if min_value > max_value:
        raise ValueError("min_value should not be greater than max_value.")

    return random.randint(min_value, max_value)


def single_element_normal_scroll(driver, locator):
    element = driver.find_element(By.CSS_SELECTOR, locator)
    driver.execute_script(
        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    random_wait()


def link_clicks(driver):
    topic_element = 'ul.content-paragraph'
    single_element_normal_scroll(driver, topic_element)

    ul_element = driver.find_element(By.CSS_SELECTOR, topic_element)
    li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
    index = get_random_number(0, len(li_elements) - 1)

    random_li = li_elements[index]
    print(f"Clicking on: {random_li.text}")
    random_li.find_element(By.TAG_NAME, 'a').click()
    random_wait()
