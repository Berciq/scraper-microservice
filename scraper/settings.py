from os.path import abspath, dirname, join

basedir = abspath(dirname(dirname(__file__)))

# For simplicity, this file contains only settings considered important 
# or that have been modified from their default.

BOT_NAME = 'scraper'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

ITEM_PIPELINES = {
    'scraper.pipelines.WebpageImagesPipeline': 1,
    'scraper.pipelines.DatabaseStoragePipeline': 2,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scraper (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Define settings for image scraping
IMAGES_EXPIRES = 0

# Define storage for images
IMAGES_STORE = '/tmp/scraper/'

# Set up database
SQLALCHEMY_DATABASE_URI = "sqlite:////" + join(basedir, 'scape_jobs.db')