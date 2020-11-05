from datetime import datetime

from api.config import db


class ScrapeJob(db.Model):
    __tablename__ = 'scrape_job'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048))
    scrape_text = db.Column(db.Boolean, default=True)
    scrape_images = db.Column(db.Boolean, default=True)
    is_finished = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    error = db.Column(db.Text, default=None)
    scraped_text = db.relationship(
        "ScrapedText",
        backref="scrape_job",
        cascade="all, delete, delete-orphan",
        uselist=False,
    )
    scraped_images = db.relationship(
        "ScrapedImage",
        backref="scrape_job",
        cascade="all, delete, delete-orphan",
        lazy='dynamic',
        order_by="asc(ScrapedImage.id)",
    )

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(cls.id == id).one_or_none()

    @classmethod
    def get_most_recent_match(cls, job):
        """
        This returns the most recent scrape job scheduled for the given URL.
        It strips off anything afater '#' to limit duplicate requests.

        :return: ScrapeJob or None if there is none
        """
        url = clean_url(job['url'])
        scrape_text = job.get('scrape_text', True)
        scrape_images = job.get('scrape_images', True)
        query = cls.query.filter(cls.url == url).order_by(cls.id.desc())
        if scrape_text:
            query = query.filter(cls.scrape_text == True)
        if scrape_images:
            query = query.filter(cls.scrape_images == True)
        return query.first()

    @classmethod
    def from_dict(cls, dic):
        job = ScrapeJob(url=clean_url(dic['url']))
        if 'scrape_text' in dic:
            job.scrape_text = dic['scrape_text']
        if 'scrape_images' in dic:
            job.scrape_images = dic['scrape_images']
        return job

    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'scrape_text': self.scrape_text,
            'scrape_images': self.scrape_images,
            'is_finished': self.is_finished,
        }


class ScrapedText(db.Model):
    __tablename__ = 'scraped_text'
    job_id = db.Column(db.Integer, db.ForeignKey("scrape_job.id"), primary_key=True)
    text = db.Column(db.Text, nullable=True)


class ScrapedImage(db.Model):
    __tablename__ = 'scraped_image'
    job_id = db.Column(db.Integer, db.ForeignKey("scrape_job.id"), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048))
    alt = db.Column(db.String(2048))
    path = db.Column(db.String)

    @classmethod
    def get_by_job_and_img_id(cls, job_id, img_id):
        return cls.query.filter(cls.job_id == job_id, cls.id==img_id).one_or_none()


def clean_url(url):
    return url.split('#')[0]
