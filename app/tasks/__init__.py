# load the tasks from the respective files for celery to discover them
from .ai_tasks import analyze_review_sentiment
from .log_tasks import log_access_task
