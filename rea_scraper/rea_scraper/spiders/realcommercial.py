import re
import json
import bs4
import scrapy
from rea_scraper.items import RealEstateListing


class SearchCategory:
    """Enumerate search categories and their corresponding url slugs.
    """
    FOR_SALE = 'for-sale'
    FOR_LEASE = 'for-lease'
    SOLD = 'sold'
    INVEST = 'invest'
    SHORT_TERM = 'short-term-workspace'
    FIND_AGENT = 'find-agent'


class RealcommercialSpider(scrapy.Spider):
    name = 'realcommercial'
    allowed_domains = ['www.realcommercial.com.au']
    PAGE_DATA = re.compile('REA.pageData = ({.*});')
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_ITEMS' :1,
        # 'CLOSESPIDER_PAGECOUNT': 20,
    }

    def start_requests(self):
        category_handlers = {
            SearchCategory.FOR_LEASE: self.parse_for_lease,
            SearchCategory.FOR_SALE: self.parse_for_sale,
        }

        # Add a CATEGORY field to separate outputs by SearchCategory
        # Field is needed as CATEGORY does not always match the pdpUrl, i.e. INVEST
        for category_slug, parser in category_handlers.items():
            category_url = f'https://www.realcommercial.com.au/{category_slug}/'
            yield scrapy.Request(
                category_url,
                callback=parser,
                cb_kwargs={'category': category_slug}
            )

    def parse_for_sale(self, response, category):
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        scripts = soup.find_all("script")
        data_script = next(s for s in scripts if "REA.pageData" in s.text)
        page_data_match = self.PAGE_DATA.search(data_script.text)
        page_data = json.loads(page_data_match.group(1))
        
        for item in page_data.get('exactMatchListings', list()):
            attributes = item.get('attributes', dict())
            address = item.get('address', dict())
            yield RealEstateListing(
                id=item.get('id'),
                title=item.get('title'),
                product=item.get('product'),
                daysActive=item.get('daysActive'),
                hasTour=item.get('hasTour'),
                pdpUrl=item.get('pdpUrl'),
                tenureType=item.get('tenureTypeObject', {}).get('key'),
                highlights=item.get('highlights', list()),
                agencies=[agency.get('name') for agency in item.get('agencies') if agency.get('name')],
                area=attributes.get('area'),
                propertyTypes=attributes.get('propertyTypes'),
                carSpaces=attributes.get('carSpaces'),
                state=address.get('state'),
                streetAddress=address.get('streetAddress'),
                postcode=address.get('postcode'),
                suburb=address.get('suburb'),
                suburbAddress=address.get('suburbAddress'),
                price=item.get('details', dict()).get('price'),
                searchCategory=category,
            )

        next_page_btn = soup.find('a', {'aria-label': 'next'})
        if next_page_btn:
            rel_path = next_page_btn.get('href', None)
            if rel_path:
                yield response.follow(
                    response.urljoin(rel_path),
                    callback=self.parse_for_sale,
                    cb_kwargs={'category': category},
                )

    def parse_for_lease(self, response, category):
        for item in self.parse_for_sale(response, category):
            yield item
