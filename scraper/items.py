import scrapy


class WebpageContentItem(scrapy.Item):
    job_id = scrapy.Field()
    text = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()