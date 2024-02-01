import json

import scrapy

from ..items import ProductItem


class SamokatSpider(scrapy.Spider):
    name = "samokat"
    custom_settings = {"CLOSESPIDER_ITEMCOUNT": 2}

    @staticmethod
    def get_links(products):
        link = "https://samokat.ru/product/"
        return (f"{link}{product_id}/" for product_id in products)

    @staticmethod
    def get_next_data_products(response):
        data = response.css("#__NEXT_DATA__::text").get()
        json_blob = json.loads(data)
        products = json_blob["props"]["pageProps"]["initialState"]["products"][
            "entities"
        ]
        return products

    def start_requests(self):
        urls = [
            "https://web.samokat.ru/",
            "https://samokat.ru/category/gotovaya-eda-sladkoe-k-chayu/",
        ]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        data = response.css("#__NEXT_DATA__::text").get()
        json_blob = json.loads(data)
        products = json_blob["props"]["pageProps"]["initialState"]["products"][
            "entities"
        ]
        links = self.get_links(products)

        yield from response.follow_all(links, callback=self.parse_product)

    def parse_product(self, response):
        products = self.get_next_data_products(response)
        product_id = response.url.split("/")[4]
        product = products[product_id]
        if product:
            title = product["name"]
            content = product["attributes"][0]["value"]
            price = product["price"]
            yield ProductItem(title=title, content=content, price=price)
