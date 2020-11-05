from api.config import db
from api.models import ScrapeJob, ScrapedText, ScrapedImage

db.create_all()