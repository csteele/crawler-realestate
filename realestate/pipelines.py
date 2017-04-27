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

class RealestatePipeline(object):
    def process_item(self, item, spider):
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
        file = open('%s_items.p' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = PickleItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        elapsed=0
        try:
            socket="http://{0}:{1}".format(item['ip'],item['port'])
            proxyDict = {"http":socket}
            response = rq.get('http://www.google.com',proxies=proxyDict,timeout=2)
            elapsed = response.elapsed
            spider.logger.info('Socket{0}\tElapsed{1}'.format(socket,elapsed))
            if elapsed>timedelta(seconds=5):
                raise DropItem("Slow connection")
        except Exception as e:
            raise DropItem("Cannot Connect")
        item["speed"] = elapsed
        item["lastcheck"] = date.today()
        self.exporter.export_item(item)
        return item