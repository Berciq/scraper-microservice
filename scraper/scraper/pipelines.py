from contextlib import suppress

from itemadapter import ItemAdapter
from PIL import UnidentifiedImageError
from scrapy.pipelines.images import ImageException, ImagesPipeline
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from scraper.models import ScrapeJob, ScrapedText, ScrapedImage


class WebpageImagesPipeline(ImagesPipeline):
    
    def file_path(self, request, response=None, info=None, *, item=None):
        path = super().file_path(request, response, info, item=item)
        return str(item['job_id']) + '/' + path

    # TODO: Because of some backwards compatibility wrapper around MediaPipeline
    # this method is not overrideing the MediaPipline method. Investigate.
    def media_downloaded(self, response, request, info, *, item=None):
        with suppress(ImageException, UnidentifiedImageError):
            return super().media_downloaded(
                response, request, info, item=item)


class DatabaseStoragePipeline:

    def __init__(self, database_uri):
        self.db_uri = database_uri
        self.db_session = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            database_uri=crawler.settings.get('SQLALCHEMY_DATABASE_URI'),
        )

    def open_spider(self, spider):
        engine = create_engine(self.db_uri, echo=False)
        Session = sessionmaker(bind=engine)
        self.db_session = Session()

    def close_spider(self, spider):
        self.db_session.close()

    def process_item(self, item, spider):
        scrape_job = self.db_session.query(ScrapeJob).get(item['job_id'])
        if item['text'] is not None:
            self.db_session.add(ScrapedText(
                scrape_job=scrape_job, 
                text=item['text'],
            ))
        for i, img in enumerate(item['images'], 1):
            self.db_session.add(ScrapedImage(
                scrape_job=scrape_job, 
                id=i,
                url=img['url'],
                path=img['path'],
            ))
        scrape_job.is_finished = True
        self.db_session.commit()
