from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from setup import utils
import random
import json

chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://sub01.gameappszone.com/")


with open('data/page_locators.json', 'r') as f:
    locators = json.load(f)

insurances = [
    "Travel",
    "Renters",
    "Liability",
    "Long-Term-Care",
    "Business",
    "Pet",
    "HomeOwners",
    "Life",
    "Health",
    "Auto",
]

selected_insurance = random.choice(insurances)


insurance_page_article_id = locators["homepage"]["titles"]["articles"].get(
    selected_insurance)
title_locator = locators["homepage"]["title"]
read_more_locator = locators["homepage"]["read-more"]
comment_locator = locators["homepage"]["comment"]

page_title = f"{insurance_page_article_id} {title_locator}"
read_more = f"{insurance_page_article_id} {read_more_locator}"
comment = f"{insurance_page_article_id} {comment_locator}"

print(f"selected page: {selected_insurance}")
print(f"page_title: {page_title}")
print(f"read_more: {read_more}")

sleep(5)
driver.find_element(By.CSS_SELECTOR, read_more).click()

sleep(5)
