import json
import scrapy
import six
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags
from collections import OrderedDict


class TutorialItem(scrapy.Item):
    def __init__(self, *args, **kwargs):
        self._values = OrderedDict()
        if args or kwargs:  # avoid creating dict for most common case
            for k, v in six.iteritems(dict(*args, **kwargs)):
                self[k] = v

    def __repr__(self):
        return json.dumps(OrderedDict(self), ensure_ascii=False)

class CVEItem(TutorialItem):
    id = scrapy.Field()
    year = scrapy.Field()
    month = scrapy.Field()

class CVEDetails(TutorialItem):
    id = scrapy.Field()
    description = scrapy.Field()
    published_date = scrapy.Field()
    source = scrapy.Field()
    base_3 = scrapy.Field()
    base_2 = scrapy.Field()

