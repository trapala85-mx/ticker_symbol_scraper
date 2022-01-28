from http.server import executable
from urllib.parse import urljoin
from webbrowser import Chrome
import scrapy
from scrapy import Spider, Request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.select import Select
from scrapy import Selector


class TikcerSpider(Spider):

    name = 'ts'
    start_urls = ['https://stockanalysis.com/stocks/']
    custom_settings = {
        'FEED_URI':'ts.json',
        'FEED_FORMAT':'json',
        'FEED_EXPORT_ENCODING':'utf-8'
    }


    def __init__(self):
        self.service = Service(executable_path='chrome_driver/chromedriver')
        self.options = ChromeOptions()
        self.options.binary_location = '/usr/bin/brave-browser'
        self.options.add_argument("headless")
        self.driver = Chrome(service = self.service, options = self.options)
        self.driver.implicitly_wait(10)
        self.driver.get('https://stockanalysis.com/stocks/')
        self.driver.implicitly_wait(5)
        select_element = self.driver.find_element_by_xpath('//select[@name="perpage"]')
        select_object = Select(select_element)
        select_object.select_by_value('10000')    
        self.driver.implicitly_wait(15)
        self.html = self.driver.page_source

   
    def parse(self, response): 
        resp = Selector(text=self.html)
        tickers = resp.xpath('//table[@id="symbol-table"]//a[starts-with(@href,"/stocks")]/text()').getall()
        names = resp.xpath('//table[@id="symbol-table"]//tr//td[2]/text()').getall()
        industries = resp.xpath('//table[@id="symbol-table"]//tr//td[3]/text()').getall()

        info = list(zip(tickers, names, industries))
       
        for t,n,i in info:
            yield {
                'company': n,
                'ticker_symbol':t,
                'industriy': i
            }
        
       
        

        
        
        
