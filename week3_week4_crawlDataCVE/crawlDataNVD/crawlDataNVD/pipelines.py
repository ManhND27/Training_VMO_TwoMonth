# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
import pymongo
from threading import Thread
import threading
# from itemadapter import ItemAdapter
import logging
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
from crawlDataNVD.items import CVEItem
from crawlDataNVD.items import CVEDetails
from crawlDataNVD.items import CVEDetailsFull

settings = get_project_settings()


class CrawldatanvdPipeline:
    __instance__ = None

    @staticmethod
    def get_instance():
        if CrawldatanvdPipeline.__instance__ is None:
            CrawldatanvdPipeline.__instance__ = CrawldatanvdPipeline()
        return CrawldatanvdPipeline.__instance__

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]

    def process_item_year_month(self, item: CVEItem):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION_1']]
        if self.collection.find({'_id': item['_id']}).limit(1).count() > 0:
            print("\n\n\n\n Exitssssss Itemmmmmmmmmmmmm \n\n\n")
            pass
        else:
            self.collection.insert(item)

    def process_item_detail(self, item: CVEDetails):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION_2']]
        i = 0
        if self.collection.find({'_id': item['_id']}).limit(1).count() > 0:
            i = i + 1
            print("\n\n\n\n Exitssssss Itemmmmmmmmmmmmm {}\n\n\n".format(i))
            print(i)
            i += 1
            pass
        else:

            self.collection.insert(item)

    def process_item_detail_full(self, item: CVEDetailsFull):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION_3']]
        if self.collection.find({'_id': item['_id']}).limit(1).count() > 0:
            print("\n\n\n\n Exitssssss Itemmmmmmmmmmmmm \n\n\n")
            # pass
        else:
            self.collection.insert(item)

class TutorialPipeline:
    def __init__(self):
        settings = get_project_settings()
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = connection[settings['MONGODB_DB']]
        self.items = []

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.items.append(dict(item))
            if len(self.items) >= get_project_settings()['NUMBER_OF_ITEMS']:
                self.insert_current_items(spider)
        return item

    def insert_current_items(self, spider):
        items = self.items
        self.items = []
        try:
            collection = self.db[spider.settings.attributes['COLLECTION_NAME'].value]
            if spider.name == "scheduler":
                for item in items:
                    collection.update({"skybox_id": item["skybox_id"]}, {"$set": item})
            else:
                collection.insert_many(items)
        except:
            logging.info("Item already in database")

    def close_spider(self, spider):
        self.insert_current_items(spider)
