import json
import scrapy
from ..items import CVEDetailsFull
from ..pipelines import CrawldatanvdPipeline
#from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import TimeoutError, TCPTimedOutError, ConnectionRefusedError
from twisted.web._newclient import ResponseFailed, ResponseNeverReceived
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.utils.response import response_status_message
from collections import defaultdict


class CVE_Detail(scrapy.Spider):
    name = "cve_detail_full"

    # start_urls = ['https://nvd.nist.gov/vuln/full-listing']

    def start_requests(self):
        data = open('./year_month_cve.json', )
        year_month_cves = json.load(data)
        url = 'https://nvd.nist.gov/vuln/detail/'
        url_ids = []
        for ymc in year_month_cves:
            url_ids.append(ymc["id"])
        for url_id in url_ids:
            url_full = url + url_id
            request = scrapy.Request(url_full, callback=self.parse, meta={'id': url_id})
            request.meta['id'] = url_id
            yield request

    def parse(self, response):
        item = CVEDetailsFull()
        item['id'] = response.meta['id']
        item['description'] = response.xpath('//p[@data-testid="vuln-description"]/text()').get()
        item['published_date'] = response.xpath('//span[@data-testid="vuln-published-on"]/text()').get()
        item['source'] = response.xpath('//span[@data-testid="vuln-current-description-source"]/text()').get()
        item['severity'] = {}
        item['severity']['cvss_ver_3x'] = {}
        item['severity']['cvss_ver_2'] = {}
        item['severity']['cvss_ver_3x']['base_score'] = response.xpath('//a[@id="Cvss3NistCalculatorAnchor"]/text()').get()
        item['severity']['cvss_ver_2']['base_score'] = response.xpath('//a[@id="Cvss2CalculatorAnchor"]/text()').get()
        request = scrapy.Request(url="https://www.vulnerabilitycenter.com/svc/svc/svc", callback=self.parse_cve_skybox, meta={'item': item})
        yield request

    def parse_cve_skybox(self, response):
        item = response.meta['item']
        try:
            item['skybox_id'] = response.text.split('","')[2]
            request = scrapy.Request(url="https://www.vulnerabilitycenter.com/svc/svc/svc",
                                     callback=self.parse_cve_skybox_full(),
                                     errback=self.errback, dont_filter=True,
                                     headers=self.get_headers_skybox(),
                                     body=self.get_body_skybox(item['skybox_id']),
                                     cookies=self.get_cookie_skybox(),
                                     meta={'item': item})
            yield request
        except:
            yield item

    def parse_cve_skybox_full(self, response):
        item = response.meta['item']
        item.update(self.get_json(response.text))
        CrawldatanvdPipeline.get_instance().process_item_detail_full(item)
        yield item

    def errback(self, failure):
        request = failure.request

        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error(
                'errback <%s> %s , response status:%s' %
                (request.url, failure.value, response_status_message(response.status))
            )
        elif failure.check(ResponseFailed):
            self.logger.error('errback <%s> ResponseFailed' % request.url)

        elif failure.check(ConnectionRefusedError):
            self.logger.error('errback <%s> ConnectionRefusedError' % request.url)

        elif failure.check(ResponseNeverReceived):
            self.logger.error('errback <%s> ResponseNeverReceived' % request.url)

        elif failure.check(TCPTimedOutError, TimeoutError):
            self.logger.error('errback <%s> TimeoutError' % request.url)

        else:
            self.logger.error('errback <%s> OtherError' % request.url)

    @staticmethod
    def get_json(text):
        mydict = lambda: defaultdict(mydict)
        dict = mydict()
        text = text.replace('"],0,7]', '')
        text = text.split('","')
        dict["vendor"] = text[text.index("Vendor") + 1]
        dict["scanner"] = text[text.index("Scanners") + 1]
        dict["affected_products"]["product"] = text[text.index("Product") + 1]
        dict["affected_products"]["category"] = text[text.index("Category") + 1]
        dict["affected_products"]["affected_versions"] = text[text.index("Affected Versions") + 1]
        dict["solutions"] = []
        try:
            dict1 = {}
            dict1["name"] = text[text.index("name") + 1]
            dict1["type"] = text[text.index("type") + 1]
            dict1["description"] = text[text.index("description") + 1]
            dict["solutions"].append(dict1)
            dict2 = {}
            dict2["name"] = text[text.index("solution") + 2]
            dict2["type"] = text[text.index("solution") + 4]
            dict2["description"] = text[text.index("solution") + 3]
            dict["solutions"].append(dict2)
            start = text.index("solution") + 6
            if start == len(text) - 1:
                dict3 = {}
                dict3["name"] = text[text.index("solution") + 2]
                dict3["type"] = text[text.index("solution") + 4]
                dict3["description"] = text[text.index("solution") + 6]
                dict["solutions"].append(dict3)
            else:
                for i in range(start, len(text) - 1, 2):
                    dict3 = {}
                    dict3["name"] = text[text.index("solution") + 2]
                    dict3["type"] = text[text.index("solution") + 4]
                    dict3["description"] = text[i]
                    dict["solutions"].append(dict3)
        except:
            pass
        yield dict


    @staticmethod
    def get_headers_skybox():
        hearder = {
            "authority": "www.vulnerabilitycenter.com",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"91\", \"Google Chrome\";v=\"91\"",
            "x-gwt-module-base": "https://www.vulnerabilitycenter.com/svc/svc/",
            "x-gwt-permutation": "938A4411868A979D515A5CE34BBE59F8",
            "sec-ch-ua-mobile": "?0",
            "content-type": "text/x-gwt-rpc; charset=UTF-8",
            "accept": "*/*",
            "origin": "https://www.vulnerabilitycenter.com",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://www.vulnerabilitycenter.com/svc/SVC.html",
            "accept-language": "en-US,en;q=0.9"
        }
        return hearder

    @staticmethod
    def get_body_skybox(id):
        body = "7|0|6|https://www.vulnerabilitycenter.com/svc/svc/|4EB3C5214EE901B9C18B44EBC7FF695D|" \
               "com.skybox.svc.shared.SVCService|getVulnerabilityRecord|java.lang.String/" \
               "2004016611|{}|1|2|3|4|1|5|6|"
        return body.format(id)

    @staticmethod
    def get_cookie_skybox():
        cookie_string = "JSESSIONID=1CC719D39466FCA3C60E7592BEAC22F0; SESS9ab004767f41bf8781a9a80db17b50c6=90mdbc9bi7ffeqlkan6aoi8475; d-a8e6=2afa44f7-9a02-4f79-9569-f03f72ef83df; __utmz=66189737.1626662324.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _mkto_trk=id:440-MPQ-510&token:_mch-vulnerabilitycenter.com-1626662324339-98950; OptanonAlertBoxClosed=2021-07-19T02:55:04.552Z; has_js=1; s-9da4=4fef12a7-a209-4eca-8dd8-2dd6b22e9b0f; __utma=66189737.538287118.1626662324.1626662324.1626687780.2; __utmc=66189737; __utmt=1; OptanonConsent=landingPath=NotLandingPage&datestamp=Mon+Jul+19+2021+16%3A52%3A13+GMT%2B0700+(Indochina+Time)&version=3.6.28&groups=1%3A1%2C2%3A1%2C3%3A1%2C4%3A1%2C0_162101%3A1%2C0_162100%3A1%2C0_162099%3A1%2C0_162105%3A1%2C0_162104%3A1%2C0_162103%3A1%2C0_162102%3A1%2C0_162109%3A1%2C0_162108%3A1%2C0_162107%3A1%2C0_162106%3A1%2C0_162113%3A1%2C0_162112%3A1%2C0_162111%3A1%2C0_162110%3A1&AwaitingReconsent=false; __utmb=66189737.4.10.1626687780"
        cookies = {}
        for cookie in cookie_string.split("; "):
            try:
                # init cookie key
                key = cookie.split("=")[0]
                # init cookie value
                val = cookie.split("=")[1]
                # parse cookie string
                cookies[key] = val
            except:
                pass
        return cookies


