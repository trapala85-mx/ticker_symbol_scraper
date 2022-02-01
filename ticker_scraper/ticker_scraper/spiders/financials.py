#Python

#Scrapy
import json
import scrapy

#Selenium


class FinancialsSpider(scrapy.Spider):


    name = 'financials_spider'
    start_urls = []


    #EXAMPLE_LINK = 'https://www.morningstar.com/stocks/xnas/intc/quote'
    BASE_LINK = 'https://www.morningstar.com/stocks/xnas/'
    

    def __init__(self):
        self.create_links()

    def parse(self, response):
        print("*" * 10)
        print(response.text)


    def create_links(self) -> list:
        with open("ts.json", "r+", encoding="utf-8") as file:
            data = json.loads(file.read())
            
            for d in data:
                self.start_urls.append(self.BASE_LINK + d['ticker_symbol'] + '/quote')
    

    def __get_exchanges(self) -> list:
        with open ('ts.json', 'r+', encoding='utf-8') as file:
            pass