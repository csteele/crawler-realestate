# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class RealestateItem(Item):
	date = Field()
	url = Field()
	address = Field()
	priceText = Field()
	bedrooms = Field()
	bathrooms = Field()
	cars = Field()
	type = Field()
	subtype = Field()
	price = Field()


class ProxyItem(Item):
	ip = Field()
	port = Field()
	type = Field()
	speed = Field()
	lastcheck = Field()

	def __repr__(self):
		"""Do not return info"""
		return repr("")
