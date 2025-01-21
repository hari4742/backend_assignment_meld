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
router = APIRouter()


@router.get("/reviews/trends", response_model=list[CategoryInResponse])
async def get_review_trends(db: Session = Depends(get_db)):

    # TODO: move this query to services and check the query validity
    result = db.query(
        Category.id,
        Category.name,
        Category.description,
        func.avg(ReviewHistory.stars).label("average_stars"),
        func.count(ReviewHistory.id).label("total_reviews")
    ).join(ReviewHistory, Category.id == ReviewHistory.category_id) \
     .group_by(Category.id) \
     .order_by(func.avg(ReviewHistory.stars).desc()) \
     .limit(5) \
     .all()

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


@router.get("/reviews/", response_model=list[ReviewHistoryInResponse])
async def get_reviews(category_id: int, page: int = 1, page_size: int = 15, db: Session = Depends(get_db)):
    offset = (page - 1) * page_size

    # TODO: move this query to services and check the query validity
    reviews = db.query(ReviewHistory).filter(ReviewHistory.category_id == category_id) \
                .order_by(ReviewHistory.created_at.desc()) \
                .offset(offset).limit(page_size).all()

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
