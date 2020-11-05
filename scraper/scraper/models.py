from datetime import datetime

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String, Table,
                        Text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

Base = declarative_base()


class ScrapeJob(Base):
    __tablename__ = 'scrape_job'
    id = Column(Integer, primary_key=True)
    url = Column(String(2048))
    scrape_text = Column(Boolean, default=True)
    scrape_images = Column(Boolean, default=True)
    is_finished = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    error = Column(Text, default=None)
    scraped_text = relationship(
        "ScrapedText",
        backref="scrape_job",
        cascade="all, delete, delete-orphan",
        uselist=False,
    )
    scraped_images = relationship(
        "ScrapedImage",
        backref="scrape_job",
        cascade="all, delete, delete-orphan",
        order_by="asc(ScrapedImage.id)",
    )


class ScrapedText(Base):
    __tablename__ = 'scraped_text'
    job_id = Column(Integer, ForeignKey("scrape_job.id"), primary_key=True)
    text = Column(Text, nullable=True)


class ScrapedImage(Base):
    __tablename__ = 'scraped_image'
    job_id = Column(Integer, ForeignKey("scrape_job.id"), primary_key=True)
    id = Column(Integer, primary_key=True)
    url = Column(String(2048))
    alt = Column(String(2048))
    path = Column(String)
