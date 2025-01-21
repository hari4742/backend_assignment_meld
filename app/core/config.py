import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Database settings
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app/db/reviews.db")

    # Celery configuration
    CELERY_BROKER_URL = os.getenv(
        "CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_BACKEND_URL = os.getenv(
        "CELERY_BACKEND_URL", "redis://localhost:6379/0")

    # OpenAI API configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

    # Pagination settings
    PAGE_SIZE = 15


settings = Settings()
