from selenium import webdriver
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(3)
        self.driver.get(url)
        self.soup = None

    def update_soup(self):
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')

    def quit(self):
        self.driver.quit()
