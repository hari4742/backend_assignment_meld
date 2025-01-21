from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    description: str


class CategoryInResponse(CategoryBase):
    id: int
    average_stars: float
    total_reviews: int

    class Config:
        from_attributes = True
