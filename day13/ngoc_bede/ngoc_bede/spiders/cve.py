import scrapy
from ngoc_bede.items import NgocBedeItem
from scrapy.loader import ItemLoader


class CveSpider(scrapy.Spider):
    name = 'cve'
    allowed_domains = ['nvd.nist.gov']
    start_urls = ['https://nvd.nist.gov/vuln/full-listing/']

    def parse(self, response):
        for year in response.xpath('//*[@id="body-section"]/div[2]').css('span:not([class])'):
            for month in year.css('a'):
                item = NgocBedeItem()
                item['year'] = year.css('strong::text').get()
                item['month'] = month.css('::text').get()
                href = month.attrib['href']
                url = response.urljoin(href)
                request = scrapy.Request(url, callback=self.parse_dir_contents)
                request.meta['item'] = item
                yield request

    @staticmethod
    def parse_dir_contents(response):
        for cve in response.xpath('//*[@id="body-section"]/div[2]/div').css('a::text'):
            item = response.meta['item']
            item['id'] = cve.get()
            yield item
