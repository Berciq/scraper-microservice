import scrapy
from bs4 import BeautifulSoup
from scraper.items import WebpageContentItem
from scraper.models import ScrapeJob
from scrapy import signals
from scrapy.exceptions import DontCloseSpider
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class ContentSpider(scrapy.Spider):
    name = "content"

    def create_request(self, scrape_job):
        return scrapy.Request(
            url=scrape_job.url, 
            callback=self.parse,
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

    def on_idle(self):
        database_uri=self.crawler.settings.get('SQLALCHEMY_DATABASE_URI')
        engine = create_engine(database_uri, echo=False)
        Session = sessionmaker(bind=engine)
        db = Session()
        for job in db.query(ScrapeJob).filter(ScrapeJob.is_finished==False):
            self.crawler.engine.crawl(self.create_request(job), self)
        db.close()
        raise DontCloseSpider()
