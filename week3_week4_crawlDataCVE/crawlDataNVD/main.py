from multiprocessing import connection
import defer
import pymongo
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet.task import react

# from crawlDataNVD.crawlDataNVD.pipelines import settings
from crawlDataNVD.spiders.cve_detail import CVE_Details
from crawlDataNVD.spiders.cve_detail_full import CVE_Detail_full
from crawlDataNVD.spiders.scheduler import SchedulerSpider
import schedule
from crawlDataNVD.spiders.scheduler import SchedulerSpider


def get_cve_len():
    settings = get_project_settings()
    connection = pymongo.MongoClient(
        settings['MONGODB_SERVER'],
        settings['MONGODB_PORT']
    )
    db = connection[settings['MONGODB_DB']]
    collections = db['year_month_cve']
    return collections.count_documents({})


if __name__ == '__main__':
    configure_logging()
    runner = CrawlerRunner(get_project_settings())


    @defer.inlineCallbacks
    def crawl():
        # yield runner.crawl(CrawYearMothCVE)
        length = get_cve_len()
        runner.crawl(CVE_Details, inp1=0, inp2=int(length / 4))
        runner.crawl(CVE_Details, inp1=int(length / 4) + 1, inp2=int(length / 2))
        runner.crawl(CVE_Details, inp1=int(length / 2) + 1, inp2=int(3 * length / 4))
        runner.crawl(CVE_Details, inp1=int(3 * length / 4) + 1, inp2=int(length))

        runner.crawl(CVE_Detail_full, inp1=0, inp2=int(length / 8))
        runner.crawl(CVE_Detail_full, inp1=int(length / 8) + 1, inp2=int(length / 4))
        runner.crawl(CVE_Detail_full, inp1=int(length / 4) + 1, inp2=int(3 * length / 8))
        runner.crawl(CVE_Detail_full, inp1=int(3 * length / 8) + 1, inp2=int(length / 2))
        runner.crawl(CVE_Detail_full, inp1=int(length / 2) + 1, inp2=int(5 * length / 8))
        runner.crawl(CVE_Detail_full, inp1=int(5 * length / 8) + 1, inp2=int(3 * length / 4))
        runner.crawl(CVE_Detail_full, inp1=int(3 * length / 4) + 1, inp2=int(7 * length / 8))
        runner.crawl(CVE_Detail_full, inp1=int(7 * length / 8) + 1, inp2=int(length))
        d = runner.join()
        yield d
        yield schedule.every().hour.do(runner.crawl(SchedulerSpider))
        reactor.stop()


    crawl()
    reactor.run()
