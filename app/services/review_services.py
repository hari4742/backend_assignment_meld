from sqlalchemy.orm import Session
from sqlalchemy.sql import func, desc
from app.models.review import ReviewHistory
from app.models.category import Category
from app.core.config import settings


def get_reviews_by_category(db: Session, category_id: int, page: int = 1, page_size: int = settings.PAGE_SIZE):
    offset = (page - 1) * page_size

    # Subquery to get the latest review for each review_id in the given category
    subquery = (
        db.query(
            ReviewHistory.review_id,
            func.max(ReviewHistory.created_at).label("latest_created_at")
        )
        .filter(ReviewHistory.category_id == category_id)
        .group_by(ReviewHistory.review_id)
        .subquery()
    )

    # Query to get the latest reviews
    reviews = (
        db.query(ReviewHistory)
        .join(
            subquery,
            (ReviewHistory.review_id == subquery.c.review_id) &
            (ReviewHistory.created_at == subquery.c.latest_created_at)
        )
        .order_by(desc(ReviewHistory.created_at))
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return reviews


def get_top_categories(db: Session, limit: int = 5):

    # Subquery to get the latest review per review_id
    subquery = (
        db.query(
            ReviewHistory.review_id,
            func.max(ReviewHistory.created_at).label("latest_created_at")
        )
        .group_by(ReviewHistory.review_id)
        .subquery()
    )

    top_categories = (
        db.query(
            Category.id,
            Category.name,
            Category.description,
            func.avg(ReviewHistory.stars).label("average_stars"),
            func.count(ReviewHistory.id).label("total_reviews")
        )
        .join(ReviewHistory, Category.id == ReviewHistory.category_id)
        .join(
            subquery,
            (ReviewHistory.review_id == subquery.c.review_id) &
            (ReviewHistory.created_at == subquery.c.latest_created_at)
        )
        .group_by(Category.id)
        .order_by(desc(func.avg(ReviewHistory.stars)))
        .limit(limit)
        .all()
    )

    return top_categories
