import json
import scrapy
from ..items import CVEDetails
from ..pipelines import CrawldatanvdPipeline
from ..items import CVEItem


class CVE_Details(scrapy.Spider):
    name = "cve_detail"

    # start_urls = ['https://nvd.nist.gov/vuln/full-listing']

    def start_requests(self):
        data = open('./year_month_cve.json')
        year_month_cves = json.load(data)
        url = 'https://nvd.nist.gov/vuln/detail/'
        url_ids = []
        for ymc in year_month_cves:
            url_ids.append(ymc["_id"])
        for url_id in url_ids:
            url_full = url + url_id
            request = scrapy.Request(url_full, callback=self.parse)
            request.meta['_id'] = url_id
            yield request

    def parse(self, response):
        item = CVEDetails()
        item['_id'] = response.meta['_id']
        item['description'] = response.xpath('//p[@data-testid="vuln-description"]/text()').get()
        item['published_date'] = response.xpath('//span[@data-testid="vuln-published-on"]/text()').get()
        item['last_modified'] = response.xpath('//span[@data-testid="vuln-last-modified-on"]/text()').get()
        item['source'] = response.xpath('//span[@data-testid="vuln-current-description-source"]/text()').get()
        item['severity'] = {}
        item['severity']['cvss_ver_3x'] = {}
        item['severity']['cvss_ver_2'] = {}
        item['severity']['cvss_ver_3x']['base_score'] = response.xpath('//a[@id="Cvss3NistCalculatorAnchor"]/text()').get()
        item['severity']['cvss_ver_2']['base_score'] = response.xpath('//a[@id="Cvss2CalculatorAnchor"]/text()').get()
        CrawldatanvdPipeline.get_instance().process_item_detail(item)
        yield item
