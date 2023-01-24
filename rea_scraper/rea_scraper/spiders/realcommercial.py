import re
import json
import bs4
import scrapy



class RealcommercialSpider(scrapy.Spider):
    name = 'realcommercial'
    allowed_domains = ['www.realcommercial.com.au']
    start_urls = ['https://www.realcommercial.com.au/for-sale/']

    def parse(self, response):
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        scripts = soup.find_all("script")
        data_script = next(s for s in scripts if "REA.pageData" in s.text)
        page_data_match = re.search('REA.pageData = ({.*});', data_script.text)
        page_data = json.loads(page_data_match.group(1))

        for listing in page_data.get('exactMatchListings', list()):
            yield listing
        next_page_btn = soup.find('a', {'aria-label': 'next'})
        if next_page_btn:
            rel_path = next_page_btn.get('href', None)
            if rel_path:
                yield response.follow(response.urljoin(rel_path), callback=self.parse)
