from collections import defaultdict
import scrapy
from pymongo import MongoClient
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.utils.project import get_project_settings
from scrapy.utils.response import response_status_message
from twisted.internet.error import TCPTimedOutError
from twisted.web._newclient import ResponseNeverReceived, ResponseFailed

from ..items import CVEDetailsFull


class SchedulerSpider(scrapy.Spider):
    name = 'scheduler'

    custom_settings = {
        'COLLECTION_NAME': 'cve_detail_full'
    }

    def __init__(self):
        settings = get_project_settings()
        connection = MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[self.custom_settings['COLLECTION_NAME']]
        self.skybox_ids = [field['skybox_id'] for field in
                           self.collection.find({"$or": [{"solutions": {"$exists": "false"}},
                                                         {"solutions": {"$size": 0}}]}, {"skybox_id": 1})]

    def start_requests(self):
        for skybox_id in self.skybox_ids:
            yield scrapy.Request(url="https://www.vulnerabilitycenter.com/svc/svc/svc",
                                 callback=self.parse_cve_skybox_full,
                                 errback=self.errback, dont_filter=True, method='POST',
                                 headers=self.get_headers_skybox(),
                                 body=self.get_body_skybox_full(skybox_id),
                                 cookies=self.get_cookie_skybox(),
                                 meta={'skybox_id': skybox_id})

    def parse_cve_skybox_full(self, response):
        item = CVEDetailsFull()
        item["skybox_id"] = response.meta['skybox_id']
        item.update(self.get_json(response.text))
        #print(item)
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
    def get_headers_skybox():
        hearder = {
            "authority": "www.vulnerabilitycenter.com",
            "sec-ch-ua": "\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"",
            "x-gwt-module-base": "https://www.vulnerabilitycenter.com/svc/svc/",
            "x-gwt-permutation": "938A4411868A979D515A5CE34BBE59F8",
            "sec-ch-ua-mobile": "?0",
            "content-type": "text/x-gwt-rpc; charset=UTF-8",
            "accept": "*/*",
            "origin": "https://www.vulnerabilitycenter.com",
            "sec-fetch-site": "same-origin",
            #"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://www.vulnerabilitycenter.com/svc/SVC.html",
            "accept-language": "en-US,en;q=0.9"
        }
        return hearder

    @staticmethod
    def get_body_skybox_full(id):
        body = "7|0|6|https://www.vulnerabilitycenter.com/svc/svc/|4EB3C5214EE901B9C18B44EBC7FF695D|" \
               "com.skybox.svc.shared.SVCService|getVulnerabilityRecord|java.lang.String/" \
               "2004016611|{}|1|2|3|4|1|5|6|"
        return body.format(id)


    @staticmethod
    def get_cookie_skybox():
        cookie_string = "JSESSIONID=24EBDA3CF68BB29A223C357850CA632C; SESS9ab004767f41bf8781a9a80db17b50c6=90mdbc9b" \
                        "i7ffeqlkan6aoi8475; d-a8e6=2afa44f7-9a02-4f79-9569-f03f72ef83df; __utmz=66189737.162666232" \
                        "4.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _mkto_trk=id:440-MPQ-510&token:_mch-" \
                        "vulnerabilitycenter.com-1626662324339-98950; OptanonAlertBoxClosed=2021-07-19T02:55:04.552Z;" \
                        " has_js=1; s-9da4=553bf9cf-158e-415e-995f-e0906646afcf; __utma=66189737.538287118.16266623" \
                        "24.1627015320.1627022831.17; __utmc=66189737; __utmt=1; OptanonConsent=landingPath=NotLandi" \
                        "ngPage&datestamp=Fri+Jul+23+2021+13:47:33+GMT+0700+(Indochina+Time)&version=3.6.28&groups=" \
                        "1:1,2:1,3:1,4:1,0_162101:1,0_162100:1,0_162099:1,0_162105:1,0_162104:1,0_162103:1,0_162102" \
                        ":1,0_162109:1,0_162108:1,0_162107:1,0_162106:1,0_162113:1,0_162112:1,0_162111:1,0_162110:1&Aw" \
                        "aitingReconsent=false; __utmb=66189737.2.10.1627022831"
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
        return dict
