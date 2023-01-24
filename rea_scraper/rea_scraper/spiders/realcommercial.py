import scrapy


class RealcommercialSpider(scrapy.Spider):
    name = 'realcommercial'
    allowed_domains = ['www.realcommercial.com.au']
    start_urls = ['http://www.realcommercial.com.au/']

    def parse(self, response):
        pass
