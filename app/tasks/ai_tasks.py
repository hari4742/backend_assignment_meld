from app.core.celery_app import celery_app
from app.db.session import get_db
from app.models.review import ReviewHistory
from app.services.llm_service import analyze_sentiment_with_llm


@celery_app.task
def analyze_review_sentiment(review_id: int, review_text: str, stars: int):
    with get_db() as db:
        review = db.query(ReviewHistory).get(review_id)
        if review:
            tone, sentiment = analyze_sentiment_with_llm(review_text, stars)
            review.sentiment = sentiment
            review.tone = tone
            db.commit()
