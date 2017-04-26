from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from realestate.items import RealestateItem
from datetime import date

class RealestateSpider(CrawlSpider):
    name = 'RealestateSpider'
    allowed_domains = ['m.realestate.com.au','realestate.com.au','www.realestate.com.au','http://www.realestate.com.au']
    start_urls = ["http://www.realestate.com.au/buy/in-beenleigh+qld+4207/list-1"]
    rules = [
        Rule(LinkExtractor(restrict_xpaths='//link[@rel="next"]',tags=('link')),callback='parse_items',follow=True),
    ]

    def parse_items(self, response):
        """
        default parse method, rule is not useful now
        """
        # import pdb; pdb.set_trace()
        self.logger.info('Hi, this is an item page! %s', response.url)
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
