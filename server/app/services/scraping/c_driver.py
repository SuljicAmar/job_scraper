import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
)
import requests
import numpy as np
from fake_useragent import UserAgent
from ..jobs import add_unparsed_job
from ...cfg import config


class SearchEngine:

    def __init__(self):
        self.set_driver()
        self._config = config()
        self.url = self._config["scrape"]

    def set_driver(self):
        ua = UserAgent()
        agent = ua.random
        opts = uc.ChromeOptions()
        opts.add_argument(f"user-agent={agent}")
        self.driver = uc.Chrome(options=opts, headless=True)

    def home(self):
        self.driver.get(self.url)

    def search(self, input):
        self.home()
        search_box = self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div[1]/div[2]/textarea",
        )
        self.waiting_strategy(search_box.send_keys(input, Keys.RETURN))

    def click(self, element):
        self.waiting_strategy(element.click())

    def get_links(self):
        div = self.driver.find_element(By.ID, "search").find_elements(
            By.TAG_NAME, "a"
        )
        return [elem.get_attribute("href") for elem in div]

    def go_to_next_page(self):
        next_page_button = self.driver.find_elements(By.CLASS_NAME, "fl")

        if len(next_page_button) < self.current_page + 1:
            self.click(next_page_button)[self.current_page + 1]
        self.current_page += 1

    def scrape_links(self, query, pages_to_scrape):
        for iPage in range(pages_to_scrape):
            self.search(query)
            add_unparsed_job(self.get_links())
            if iPage != pages_to_scrape - 1:
                self.go_to_next_page()
        self.quit()

    def waiting_strategy(self, method):
        time.sleep(np.random.uniform(0.75, 5))
        errors = [NoSuchElementException, ElementNotInteractableException]
        wait = WebDriverWait(
            self.driver,
            timeout=2,
            poll_frequency=0.2,
            ignored_exceptions=errors,
        )
        wait.until(lambda d: method or True)

    def quit(self):
        self.driver.quit()
