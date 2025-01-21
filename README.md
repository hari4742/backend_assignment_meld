# Python Backend Assignment

### Environment Variables

```bash
DATABASE_URL=sqlite:///./app/db/reviews.db
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_BACKEND_URL=redis://localhost:6379/0
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-4
```

### Steps to run locally

1. Clone the repo
2. Create virtual environment

```bash
python -m venv venv
.\venv\Scripts\activate  # on linux or mac: source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run database migrations

```bash
alembic upgrade head
```

5. Start Redis server (ensure Redis is installed)

```bash
redis-server
```

6. Start the Celery worker

```bash
celery -A app.core.celery_app worker --loglevel=info --pool=solo
```

7. Run the FastAPI application

```bash
uvicorn app.main:app --reload
```
