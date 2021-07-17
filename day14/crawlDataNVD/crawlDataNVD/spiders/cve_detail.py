import json
import scrapy
from scrapy.loader import ItemLoader
from crawlDataNVD.items import CVEDetails

class CVE_Detail(scrapy.Spider):
    name = "cve_detail"
    # start_urls = ['https://nvd.nist.gov/vuln/full-listing']

    def start_requests(self):
        f = open('year_month_cve.json')
        data = json.load(f)
        url = 'https://nvd.nist.gov/vuln/detail/'
        url_tails = []
        for i in data:
            url_tails.append(i["id"])
        for i in url_tails:
            url_full = url + i
            request = scrapy.Request(url_full, callback=self.parse)
            request.meta['id'] = i
            yield request

    def parse(self, response):
            item = CVEDetails()
            item['id'] = response.meta['id']
            item['description'] = response.xpath('//p[@data-testid="vuln-description"]/text()').get()
            item['published_date'] = response.xpath('//span[@data-testid="vuln-published-on"]/text()').get()
            item['last_modified'] = response.xpath('//span[@data-testid="vuln-last-modified-on"]/text()').get()
            item['source'] = response.xpath('//span[@data-testid="vuln-current-description-source"]/text()').get()
            yield item



