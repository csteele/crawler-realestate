# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy import signals
from scrapy.exceptions import DropItem
from scrapy.exporters import PickleItemExporter
import requests as rq
from datetime import date,timedelta
import string, re

class RealestatePipeline(object):

    def __init__(self):
        self.PROPERTY_TYPES = ['property', 'project']
        self.PROPERTY_SUBTYPES = ['townhouse', 'unitblock', 'house', 'unit', 'apartment', 'residential+land', 'acerage',
                                  'livestock']

    def process_item(self, item, spider):
	    item['date'] = date.today()
	    url = item['url']
	    if (url != None):
		    for types in self.PROPERTY_TYPES:
			    if types in url:
				    item["type"] = types
				    break
		    for types in self.PROPERTY_SUBTYPES:
			    if types in url:
				    item["subtype"] = types
				    break
	    priceText = item['priceText']
	    if (priceText != None):
		    index = priceText.find("$")
		    if (index != -1):
			    sub = priceText[index:]
			    allow = string.digits + "$\-,"
			    sub = re.sub('[^%s]' % allow, '', sub)
			    item["price"] = sub
	    return item


class ProxyPipeline(object):

    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
         pipeline = cls()
         crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
         crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
         return pipeline

    def spider_opened(self, spider):
        file = open('data/%s_Items.p' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = PickleItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        if item['type'] == 'transparent':
            raise DropItem("Transparent Proxy Dropped")
        try:
            socket="http://{0}:{1}".format(item['ip'],item['port'])
            proxyDict = {"http":socket}
            response = rq.get('http://www.google.com',proxies=proxyDict,timeout=2)
            elapsed = response.elapsed
            spider.logger.info('Socket{0}\tElapsed{1}'.format(socket,elapsed))
            if not ( 200 <= response.status_code < 300):
                raise DropItem("Not valid respose")
            if elapsed>timedelta(seconds=5):
                raise DropItem("Slow connection")
        except Exception as e:
            raise DropItem("Cannot Connect")
        item["speed"] = elapsed
        item["lastcheck"] = date.today()
        self.exporter.export_item(item)
        return item