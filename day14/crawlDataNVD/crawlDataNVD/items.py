import scrapy

class CVEItem(scrapy.Item):
    _id = scrapy.Field()
    year = scrapy.Field()
    month = scrapy.Field()

class CVEDetails(scrapy.Item):
    _id = scrapy.Field()
    sky_id = scrapy.Field()
    description = scrapy.Field()
    published_date = scrapy.Field()
    last_modified = scrapy.Field()
    source = scrapy.Field()
    severity = scrapy.Field()

class CVEDetailsFull(scrapy.Item):
    _id = scrapy.Field()
    skybox_id = scrapy.Field()
    description = scrapy.Field()
    published_date = scrapy.Field()
    last_modified = scrapy.Field()
    source = scrapy.Field()
    severity = scrapy.Field()
    vendor = scrapy.Field()
    scanner = scrapy.Field()
    affected_products = scrapy.Field()
    solutions = scrapy.Field()
