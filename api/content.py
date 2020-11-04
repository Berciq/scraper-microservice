import os
from config import db, IMAGES_STORE
from models import ScrapeJob, ScrapedImage
from flask import abort, redirect

def get_text(job_id):
    existing_job = ScrapeJob.get_by_id(job_id)
    if existing_job is None:
        abort(404, f"Scrape Job not found for ID: {job_id}")
    elif existing_job.scraped_text is not None:
        return existing_job.scraped_text.text, 200
    else:
        abort(404, f"No text was downloaded as part of scrape job ID: {job_id}")

def get_images(job_id):
    existing_job = ScrapeJob.get_by_id(job_id)
    if existing_job is None:
        abort(404, f"Scrape Job not found for ID: {job_id}")
    if existing_job.scraped_images is not None:
        return [img.id for img in existing_job.scraped_images], 200

def get_image(job_id, image_id):
    existing_job = ScrapeJob.get_by_id(job_id)
    if existing_job is None:
        abort(404, f"Scrape Job not found for ID: {job_id}")
    img = existing_job.scraped_images.filter(ScrapedImage.id==image_id).one_or_none()
    if img is None:
        abort(404, f"Image not found for ID: {image_id}")
    return open(os.path.join(IMAGES_STORE, img.path), 'rb').read()

