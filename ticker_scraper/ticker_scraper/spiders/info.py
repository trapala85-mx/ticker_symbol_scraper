# Project
from asyncio.log import logger
from ticker_scraper.items import CompanyItem

# Python
import json
import logging

# Scrapy
import scrapy

# --------------------------------------------------------------------------------------------------------------
class InfoSpider(scrapy.Spider):
    '''
        Spider in charge to extract the info of each company using the ticker symbol, extrating from
        yahoo finance
    '''
    
    # Constants
    COMPANY_NAME_XPATH = ''
    BASE_URL = 'https://finance.yahoo.com/quote/{}/profile?p={}'
    
    
    # Variables
    name = 'info_spider'
    custom_settings = {
        'FEED_URI': 'company.json',
        'FEED_FORMAT': 'json',
        'FEED_ENCDING_FORMAT': 'urf-8',
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
    }


    def start_requests(self):
        """Method in charge to send to the parse method each url

        Yields:
            [Request]: send each request to scrapy engine
        """        

        # Gettings tickers
        tickers = self.__get_tickers() # Hasta aquí OK
        #self.log(print(tickers), logging.WARNNG)

        # Cathces all the links creates in the method to start request
        urls_tuple = self.__get_urls(tickers) #Hasta aquí OK
        #self.log(print(urls_tuple), logging.WARNNG) 
        
        
        # sends to the scrapy engine each url to request them and send the response to the
        # parse method
        self.log(print(len(urls_tuple)), logging.WARNING)
        for i in range(5):
            #self.log(print(urls_tuple[i]), logging.WARNING) 
            yield scrapy.Request(urls_tuple[i], cb_kwargs={'ticker': tickers[i]})



    def parse(self, response, **kwargs):
        
        # Creating an CompanyItem from items.py
        item = CompanyItem()

        # Extracting info with xpath
        item['name'] = response.xpath('//div[@data-test="qsp-profile"]/h3[@class="Fz(m) Mb(10px)"]/text()').get()
        item['ticker'] = kwargs['ticker']
        item['sector'] = response.xpath('//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/span[2]/text()').get()
        item['industry'] = response.xpath('//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/span[4]/text()').get()
        item['web_page'] = response.xpath('//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[1]/a[2]/@href').get()
        item['company_resume'] = response.xpath('//*[@id="Col1-0-Profile-Proxy"]/section/section[2]/p/text()').get()
        
        yield item


    
    def __get_tickers(self) -> tuple:
        '''
            Method that extracts the tickers from the final_ticker__symbols.json

            Returns:
                (tuple): a tuple of the tickers
        '''
        try:
            with open("final_ticker_symbols.json", 'r+', encoding='utf-8') as file:
                
                # Using loads because the "file" is a Json File
                tickers = json.load(file)
                
                # The data is a list, so we pass it to a tuple because it wont be modified just read
                tickers = tuple(tickers)
                return tickers
        except OSError:
            self.log(print("file not found"), logging.WARNING)
            print('file not found')



    def __get_urls(self, tickers:tuple) -> tuple:
        '''
            Method in charge to create urls using the BASE_URL and each ticker from the tickers list

            Arguments:
                (tuple): a tuple of the tickers

            Returns:
                (tuple) : A list of urls of each ticker symbol
        '''
        urls_list = []
        
        for ticker in tickers:
            url = self.BASE_URL.format(ticker, ticker)
            urls_list.append(url)
         
        return tuple(urls_list)