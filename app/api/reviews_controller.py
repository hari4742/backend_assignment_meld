from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.category import Category
from app.models.review import ReviewHistory
from app.tasks.log_tasks import log_access_task
from app.schemas.category import CategoryInResponse
from app.schemas.review import ReviewHistoryInResponse
from app.tasks.ai_tasks import analyze_review_sentiment
from app.core.config import settings
from app.services.review_services import get_reviews_by_category, get_top_categories
router = APIRouter()


@router.get("/trends", response_model=list[CategoryInResponse])
async def get_review_trends():
    with get_db() as db:
        result = get_top_categories(db)

    log_access_task.delay("GET /reviews/trends")

    return [
        CategoryInResponse(
            id=cat.id,
            name=cat.name,
            description=cat.description,
            average_stars=cat.average_stars,
            total_reviews=cat.total_reviews
        )
        for cat in result
    ]


@router.get("/", response_model=list[ReviewHistoryInResponse])
async def get_reviews(category_id: int, page: int = 1, page_size: int = settings.PAGE_SIZE):
    with get_db() as db:
        reviews = get_reviews_by_category(
            db, category_id, page, page_size)

    log_access_task.delay(f"GET /reviews/?category_id={category_id}")

    for review in reviews:
        if not review.tone or not review.sentiment:
            analyze_review_sentiment.delay(
                review.id, review.text, review.stars)

    return [
        ReviewHistoryInResponse(
            id=review.id,
            text=review.text,
            stars=review.stars,
            review_id=review.review_id,
            created_at=review.created_at,
            tone=review.tone or "Analyzing...",
            sentiment=review.sentiment or "Analyzing...",
            category_id=review.category_id
        )
        for review in reviews
    ]
