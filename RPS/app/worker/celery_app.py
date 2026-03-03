import os
from celery import Celery

# Uses Redis as the broker and result backend. Ensure Redis is running locally on port 6379.
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "rps_worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Optional: define task routing if we scale to multiple queues for NER vs Embeddings
# celery_app.conf.task_routes = {'app.worker.tasks.*': {'queue': 'ml_queue'}}
