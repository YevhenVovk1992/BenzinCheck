import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup


class SeleniumWebDriverChrom:
    def __init__(self, link):
        self.link = link
        self.path_to_driver = os.path.join(os.path.abspath(__file__), 'selenium_drivers/chromedriver.exe')
        self.browser = webdriver.Chrome(executable_path=self.path_to_driver)

    def __enter__(self):
        self.browser.get(self.link)
        return self.browser

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_val:
            self.browser.quit()


def parse_page(html):
    data = []
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('div', {"id": "PricesTableContainer"})
    rows = table.find_all('tr')
    last = None
    last_name = None
    last_price = None
    for i in rows:
        price = i.find('h4')
        name = i.find('p6')
        if price:
            last = 'pr'
            last_price = price.text
        if name:
            last = 'na'
            last_name = name.text
        if last == 'na' and (name or price):
            data.append((last_name, last_price))
    return data


def run_selenium_task(link: str) -> list:
    result_list = []
    with SeleniumWebDriverChrom(link) as browser:
        browser.implicitly_wait(4)
        for i in range(1, 25):
            fuel_dict = {}
            browser.find_element(By.XPATH, '//*[@id="dd"]/div').click()
            region = browser.find_element(By.XPATH, f'//*[@id="dd"]/ul/li[{i}]/a')
            region_name = region.text
            region.click()
            for o in range(1, 9):
                fuel = browser.find_element(By.XPATH, f'//*[@id="price_bar_{o}"]')
                fuel.click()
                fuel = fuel.find_element(By.XPATH, f'//*[@id="price_title_{o}"]').text
                row_data = parse_page(browser.page_source)
                fuel_dict[fuel] = row_data
            result_list.append({region_name: fuel_dict})
    return result_list


if __name__ == '__main__':
    page_link = 'https://vseazs.com/'
    run_selenium_task(page_link)
