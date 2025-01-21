from fastapi import FastAPI
from app.api.reviews_controller import router as api_router

app = FastAPI()


app.include_router(api_router, prefix="/reviews", tags=["reviews"])
