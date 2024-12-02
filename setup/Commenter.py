import random
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from faker import Faker
import json

fake = Faker()


class Commenter:
    def __init__(self, driver):
        self.driver = driver

        with open('data/page_locators.json', 'r') as f:
            self.locators = json.load(f)

    def enter_comment(self, by=By.CSS_SELECTOR):

        comment_box = self.locators["insurance_page"]["comment_box"]["comment"]
        author = self.locators["insurance_page"]["comment_box"]["author"]
        email = self.locators["insurance_page"]["comment_box"]["email"]
        website = self.locators["insurance_page"]["comment_box"]["website"]

        # Fill in the comment box
        comment_box_element = self.driver.find_element(by, comment_box)
        comment_box_element.clear()
        comment_box_element.send_keys(fake.text())

        # Fill in the author
        comment_field = self.driver.find_element(by, author)
        comment_field.clear()
        comment_field.send_keys(fake.name())

        # Fill in the email
        email_field = self.driver.find_element(by, email)
        email_field.clear()
        email_field.send_keys(fake.email())

        # Fill in the website
        website_field = self.driver.find_element(by, website)
        website_field.clear()
        website_field.send_keys(fake.url())
