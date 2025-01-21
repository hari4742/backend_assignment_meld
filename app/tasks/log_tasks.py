from app.core.celery_app import celery_app
from app.db.session import get_db
from app.models.access_log import AccessLog
import datetime


@celery_app.task
def log_access_task(log: str):
    with get_db() as db:
        access_log = AccessLog(
            text=log,
            created_at=datetime.datetime.now(datetime.timezone.utc)
        )
        db.add(access_log)
        db.commit()
        db.refresh(access_log)
        return access_log
