# Python
import json
from lib2to3.pgen2 import driver
from typing_extensions import Self

# Scrapy
import scrapy
from scrapy import Selector

# Selenium
from webbrowser import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.select import Select

# --------------------------------------------------------------------------------------------------------------
class InfoSpider(scrapy.Spider):
    
    start_urls = ['https://finance.yahoo.com/']
    name = 'info_spider'
    # CONSTANTS
    COMPANY_NAME_XPATH = ''


    def __init__(self):
        self.__config_selenium()
        self.__create_list_from_file()


    def __create_list_from_file(self):
        with open("final_ticker_symbols.json", "r", encoding='utf-8') as file:
            data = json.load(file)

        for ticker in data:
            url = "https://finance.yahoo.com/quote/" + ticker + "/profile?p=" + ticker
            self.start_urls.append(url)


    def parse(self, response):
        self.driver.get(self.start_urls[0])
        self.driver.implicitly_wait(10)
        self.html = self.driver.page_source
        resp = Selector(text=self.html)
        yield {
            'page': resp.text
        }

    def __config_selenium(self):
        self.service = Service(executable_path='chrome_driver/chromedriver')
        self.options = ChromeOptions()
        self.options.binary_location = '/usr/bin/brave-browser'
        self.options.add_argument("headless")
        self.driver = Chrome(service = self.service, options = self.options)
        self.driver.implicitly_wait(10)