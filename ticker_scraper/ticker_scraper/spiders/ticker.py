#Python


#Scrapy
from scrapy import Spider
from scrapy import Selector

#Selenium
from webbrowser import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.select import Select
from selenium import webdriver


class TikcerSpider(Spider):

    name = 'ts'
    start_urls = ['https://stockanalysis.com/stocks/']
    custom_settings = {
        'FEED_URI':'ts.json',
        'FEED_FORMAT':'json',
        'FEED_EXPORT_ENCODING':'utf-8'
    }

    #CONSTANTS
    TICKER_XPATH_EXPRESSION = '//table[@id="symbol-table"]//a[starts-with(@href,"/stocks")]/text()'
    COMPANY_XPATH_EXPRESSION = '//table[@id="symbol-table"]//tr//td[2]/text()'
    INDUSTRY_XPATH_EXPRESSION = '//table[@id="symbol-table"]//tr//td[3]/text()'
    SELECT_ELEMENT_XPATH_EXPRESSION = '//select[@name="perpage"]'


    def __selenium_conf__(self) -> None:
        """
            Configures the Driver for selenium by sending the path of the driver inside this project
            using Chrome Options but using brave browser
        """        
        self.service = Service(executable_path='chrome_driver/chromedriver')
        self.options = ChromeOptions()
        self.options.binary_location = '/usr/bin/brave-browser'
        self.options.add_argument("headless")
        self.driver = Chrome(service = self.service, options = self.options)
        self.driver.implicitly_wait(10)


    def __init__(self):
        """
            Initialize configuration of Selenium and gets the response from the url in start_urls list
            then, waits for the page load and get the <select> Web Element and gets the final page to
            be scrapped in parse method
        """        
        self.__selenium_conf__()
        self.driver.get(self.start_urls[0])
        self.driver.implicitly_wait(5)
        select_element = self.__get_select_web_element()
        self.__get_page(select_element)
        

   
    def parse(self, response): 
        """
            Gets the request from selenium (self.html) and uses to scrap the info required

        Args:
            response (HtmlResponse): Receives the response from the start_url request

        Yields:
            dictionary: Gets the information of company name. ticker symbol and Industry
                        and stores in a dictionary
        """        
        resp = Selector(text=self.html)
        tickers = resp.xpath(self.TICKER_XPATH_EXPRESSION).getall()
        names = resp.xpath(self.COMPANY_XPATH_EXPRESSION).getall()
        industries = resp.xpath(self.INDUSTRY_XPATH_EXPRESSION).getall()

        info = list(zip(tickers, names, industries))

        for t,n,i in info:
            yield {
                'company': n,
                'ticker_symbol':t,
                'industriy': i
            }
    
    def __get_select_web_element(self):
        """Method to get the <select> Web Element to use it and select the option needed

        Returns:
            WebElement: return a <select> Web Element
        """        
        return self.driver.find_element_by_xpath(self.SELECT_ELEMENT_XPATH_EXPRESSION)


    def __get_page(self, element):
        """
            Uses the <select> Web Element and select the option to see 1000 ticker symbols
            in the table. Then waits to reload and grab the actual html and stores it to
            be used in parse method

        Args:
            element (WebElement): Receives the WebElement to be manipulated to get to the
                                  needed page and extract info
        """        
        select_object = Select(element)
        select_object.select_by_value('10000')    
        self.driver.implicitly_wait(15)
        self.html = self.driver.page_source
        self.html
