# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    ticker = scrapy.Field()
    web_page = scrapy.Field()
    sector = scrapy.Field()
    industry = scrapy.Field()
    company_resume = scrapy.Field()
    
