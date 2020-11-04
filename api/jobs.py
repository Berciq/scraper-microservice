from config import db
from models import ScrapeJob
from flask import abort, redirect

def create(job):
    if not job.get('scrape_text', True) and not job.get('scrape_images', True):
        abort(400, "Either 'scrape_text' or 'scrape_images' must be true.")

    existing_job = ScrapeJob.get_most_recent_by_url(job['url'])
    if existing_job is None or existing_job.is_finished and job.get('force_new', False):
        new_job = ScrapeJob.from_dict(job)
        db.session.add(new_job)
        db.session.commit()
        return new_job.to_dict(), 201
    else:
        return redirect(
            '/scrape-jobs/' + str(existing_job.id), 
            code=303,
        )

def get_status(job_id):
    existing_job = ScrapeJob.get_by_id(job_id)
    if existing_job is not None:
        return existing_job.to_dict(), 200
    else:
        abort(404, f"Scrape Job not found for ID: {job_id}")
