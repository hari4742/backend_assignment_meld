from sqlalchemy import Column, BigInteger, String, Integer, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from app.db.session import Base


class ReviewHistory(Base):
    __tablename__ = "review_history"

    id = Column(BigInteger().with_variant(Integer, "sqlite"),
                primary_key=True, autoincrement=True)
    text = Column(String, nullable=True)
    stars = Column(Integer, nullable=False)
    review_id = Column(String(255), nullable=False, index=True)
    tone = Column(String(255), nullable=True)
    sentiment = Column(String(255), nullable=True)
    category_id = Column(BigInteger, ForeignKey("category.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())
    __table_args__ = (
        CheckConstraint('stars >= 1 AND stars <= 10',
                        name='check_stars_range'),
    )
