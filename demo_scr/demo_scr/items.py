# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy.item import Field, Item


class ProductItem(Item):
    title = Field()
    content = Field()
    price = Field()
