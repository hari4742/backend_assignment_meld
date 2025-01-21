from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ReviewHistoryBase(BaseModel):
    text: Optional[str]
    stars: int
    review_id: str
    tone: Optional[str]
    sentiment: Optional[str]
    category_id: int


class ReviewHistoryInResponse(ReviewHistoryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
