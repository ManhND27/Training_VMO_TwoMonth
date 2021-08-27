import scrapy

from ..pipelines import CrawldatanvdPipeline
from ..items import CVEItem

class CrawYearMothCVE(scrapy.Spider):
    name = "year_month_cve"
    start_urls = ['https://nvd.nist.gov/vuln/full-listing']

    def parse(self, response):
        years = response.xpath('//*[@id="body-section"]/div[2]').css('span:not([class])')
        for year in years:
            months = year.css('a')
            for month in months:
                item = CVEItem()
                item['year'] = year.css('strong::text').get()
                item['month'] = month.css('::text').get()
                href = month.attrib['href']
                url = response.urljoin(href)
                request = scrapy.Request(url, callback=self.parse_dir_contents)
                request.meta['item'] = item
                yield request

    @staticmethod
    def parse_dir_contents(response):
        cves =  response.xpath('//*[@id="body-section"]/div[2]/div').css('a::text')
        for cve in cves:
            item = response.meta['item']
            item['_id'] = cve.get()
            print(type(item))
            CrawldatanvdPipeline.get_instance().process_item_year_month(item)
            yield item



