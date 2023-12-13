# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SrealityItem(scrapy.Item):
    """Scrapy Item class representing real estate data scraped from Sreality website."""
    title = scrapy.Field()
    images = scrapy.Field()
