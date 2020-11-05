import scrapy
from bs4 import BeautifulSoup
from scraper.items import WebpageContentItem
from scraper.models import ScrapeJob
from scrapy import signals
from scrapy.exceptions import DontCloseSpider
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DbSession():
    def __init__(self, database_uri):
        engine = create_engine(database_uri, echo=False)
        Session = sessionmaker(bind=engine)
        self.session = Session()
    def __enter__(self):
        return self.session
    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()


class ContentSpider(scrapy.Spider):
    name = "content"

    def create_request(self, scrape_job):
        return scrapy.Request(
            url=scrape_job.url, 
            callback=self.parse,
            errback=self.handle_failure,
            meta={
                'job_id': scrape_job.id,
                'scrape_text': scrape_job.scrape_text,
                'scrape_images': scrape_job.scrape_images,
            },
            dont_filter=True,
        )

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.on_idle, signal=scrapy.signals.spider_idle)
        return spider

    def parse(self, response):
        item = WebpageContentItem(job_id=response.meta['job_id'])
        
        # Extract webpage text
        if response.meta['scrape_text']:
            soup = BeautifulSoup(response.body, features="lxml")
            text = soup.get_text()
            item['text'] = text
        
        # Extract webpage images
        if response.meta['scrape_images']:
            item['image_urls'] = [
                response.urljoin(url) 
                for url in response.xpath('//img/@src').extract()
            ]

        yield item

    def handle_failure(self, failure):
        job_id = failure.request.meta['job_id']
        with DbSession(self.crawler.settings['SQLALCHEMY_DATABASE_URI']) as db:
            job = db.query(ScrapeJob).filter(ScrapeJob.id==job_id).one_or_none()
            job.is_finished= True
            job.error = str(failure.value)
            db.commit()

    def on_idle(self):
        with DbSession(self.crawler.settings['SQLALCHEMY_DATABASE_URI']) as db:
            for job in db.query(ScrapeJob).filter(
                        ScrapeJob.is_finished==False, 
                        ScrapeJob.error==None):
                self.crawler.engine.crawl(self.create_request(job), self)
        raise DontCloseSpider()
