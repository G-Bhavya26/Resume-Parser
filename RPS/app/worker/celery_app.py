from celery import Celery
import os

# We will use Redis as the message broker
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "crms_resume_worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=['app.worker.tasks']
)

# Optional configuration to make tasks more reliable
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    # In a real heavy ML workload, you'd want rate limits or concurrency controls here
)
