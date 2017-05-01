from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from realestate.items import RealestateItem
from datetime import date
import pickle

LOCATION_PICKLE_PATH='../data/locations.p'
BASE_URL = "http://www.realestate.com.au/buy/in-"

class RealestateSpider(CrawlSpider):
    name = 'RealestateSpider'
    allowed_domains = ['realestate.com.au','www.realestate.com.au','http://www.realestate.com.au']
    rules = [
        Rule(LinkExtractor(restrict_xpaths='//link[@rel="next"]',tags='link'),callback='parse_items',follow=True),
    ]

    custom_settings={
        "DOWNLOAD_DELAY": 3,
        "DEPTH_LIMIT": 20,
        "RETRY_TIMES": 2,
        "DOWNLOAD_TIMEOUT": 60,
        "COOKIES_ENABLED": False,
        "DOWNLOADER_MIDDLEWARES": {
            'realestate.middleware.CustomHttpProxyMiddleware': 543,
            'realestate.middleware.CustomUserAgentMiddleware': 545,
        }
    }

    def __init__(self):
        super().__init__()
        self.start_urls=self.get_start_urls(LOCATION_PICKLE_PATH,BASE_URL)

    def parse_items(self, response):
        """
        default parse method, rule is not useful now
        """
        # import pdb; pdb.set_trace()
        self.logger.info('Item Page %s', response.url)
        for sel in response.xpath('.//article[contains(@class,"resultBody")]'):
            item = RealestateItem()
            item['date'] = date.today()
            item['url'] = sel.xpath('.//a[contains(@rel,"listingName")]/@href').extract()
            item['address'] = sel.xpath('.//a[contains(@rel,"listingName")]/text()').extract()
            item['priceText'] = sel.xpath('.//p[@class="priceText"]/text()').extract()
            item['bedrooms'] = sel.xpath('.//dd[1]/text()').extract()
            item['bathrooms'] = sel.xpath('.//dd[2]/text()').extract()
            item['cars'] = sel.xpath('.//dd[3]/text()').extract()
            yield item

    def get_start_urls(self,pickle_path,base_url):
        with open(pickle_path,"rb") as file:
            locations = pickle.load(file)
            start_urls = []
            for location in locations:
                url = base_url + str(location) + '-qld/list-1'
                start_urls.append(url)
                print(url)
            return start_urls





