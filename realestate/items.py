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
    
