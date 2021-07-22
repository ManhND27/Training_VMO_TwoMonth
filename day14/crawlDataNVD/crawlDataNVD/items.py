import scrapy

# class TutorialItem(scrapy.Item):
#     def __init__(self, *args, **kwargs):
#         self._values = OrderedDict()
#         if args or kwargs:  # avoid creating dict for most common case
#             for k, v in six.iteritems(dict(*args, **kwargs)):
#                 self[k] = v
#
#     def __repr__(self):
#         return json.dumps(OrderedDict(self), ensure_ascii=False)

class CVEItem(scrapy.Item):
    id = scrapy.Field()
    year = scrapy.Field()
    month = scrapy.Field()

class CVEDetails(scrapy.Item):
    id = scrapy.Field()
    sky_id = scrapy.Field()
    description = scrapy.Field()
    published_date = scrapy.Field()
    last_modified = scrapy.Field()
    source = scrapy.Field()
    severity = scrapy.Field()

class CVEDetailsFull(scrapy.Item):
    id = scrapy.Field()
    sky_id = scrapy.Field()
    description = scrapy.Field()
    published_date = scrapy.Field()
    last_modified = scrapy.Field()
    source = scrapy.Field()
    severity = scrapy.Field()
    vendor = scrapy.Field()
    scanner = scrapy.Field()
    affected_products = scrapy.Field()
    solutions = scrapy.Field()





