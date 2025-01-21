from celery import Celery

# TODO: move this to config file
REDIS_URL = "redis://localhost:6379/0"
celery_app = Celery(
    "app",
    broker=REDIS_URL,
    backend=REDIS_URL,
)
