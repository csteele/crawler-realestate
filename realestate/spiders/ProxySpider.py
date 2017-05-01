from scrapy.http import Request
from scrapy.spiders import Spider
from realestate.items import ProxyItem
from datetime import date

class ProxySpider(Spider):
	name = 'ProxySpider'

	custom_settings={
		"DOWNLOAD_DELAY": 2,
		"DEPTH_LIMIT": 1,
		"RETRY_TIMES": 0,
		"DOWNLOAD_TIMEOUT": 10,
		"COOKIES_ENABLED": False,
		"FEED_FORMAT": "pickle",
		"ITEM_PIPELINES": {'realestate.pipelines.ProxyPipeline': 300}
	}

	def start_requests(self):
		urls = ['http://www.us-proxy.org', 'http://www.free-proxy-list.net/uk-proxy.html', 'http://www.socks-proxy.net/']
		for url in urls:
			yield Request(url=url, callback=self.parse)

	def parse(self, response):
		self.logger.info('Item Page %s', response.url)
		for sel in response.xpath('//table[@id="proxylisttable"]//tr'):
			item = ProxyItem()
			item['ip'] = sel.xpath('.//td[1]//text()').extract_first()
			item['port'] = sel.xpath('.//td[2]/text()').extract_first()
			item['type'] = sel.xpath('.//td[5]/text()').extract_first()
			item['speed'] = ''
			item['lastcheck'] = ''
			yield item
