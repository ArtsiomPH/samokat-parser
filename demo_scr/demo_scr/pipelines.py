# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from psycopg2 import connect

from .settings import DB_SETTINGS


class PostgresPipeline:
    def __init__(self):
        self.conn = connect(
            host=DB_SETTINGS.get("HOST"),
            user=DB_SETTINGS.get("USER"),
            password=DB_SETTINGS.get("PASSWORD"),
            database=DB_SETTINGS.get("DATABASE"),
            port=DB_SETTINGS.get("PORT"),
        )

        self.cur = self.conn.cursor()

        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS goods(
            id serial NOT NULL,
            title varchar,
            description varchar,
            price decimal,
            PRIMARY KEY (id)
        )
        """
        )

    def process_item(self, item, spider):
        self.cur.execute(
            """ insert into goods (title, description, price) values (%s,%s,%s)""",
            (
                item["title"],
                item["content"],
                float(item["price"]),
            ),
        )

        self.conn.commit()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
