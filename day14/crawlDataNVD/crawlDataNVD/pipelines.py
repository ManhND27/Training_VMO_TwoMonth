# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
import pymongo
# from itemadapter import ItemAdapter
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
        self.collection = db[settings['MONGODB_COLLECTION_1']]
        self.collection = db[settings['MONGODB_COLLECTION_2']]
        self.collection = db[settings['MONGODB_COLLECTION_3']]
    def process_item(self, item:CVEItem):
        if self.collection.find({'_id': item['_id']}).limit(1).count() > 0:
            print("\n\n\n\n Exitssssss Itemmmmmmmmmmmmm \n\n\n")
            # pass
        else:
            self.collection.insert(item)

    def process_item_detail(self, item:CVEDetails):

        if self.collection.find({'_id': item['_id']}).limit(1).count() > 0:
            print("\n\n\n\n Exitssssss Itemmmmmmmmmmmmm \n\n\n")
            # pass
        else:
            self.collection.insert(item)



    def process_item_detail_full(self, item:CVEDetailsFull):
        # valid = True
        # for key, value in item.items():
        #     if not value:
        #         valid = False
        #         raise DropItem("Missing {0}!".format(value))
        # if valid:
        #     self.collection.insert_one(dict(item))
        #
        # return item
        if self.collection.find({'_id': item['_id']}).limit(1).count() > 0:
            print("\n\n\n\n Exitssssss Itemmmmmmmmmmmmm \n\n\n")
            # pass
        else:
            self.collection.insert(item)
