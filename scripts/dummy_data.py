import random
from datetime import datetime, timedelta
from app.db.session import get_db
from app.models.category import Category
from app.models.review import ReviewHistory
from sqlalchemy.orm import Session

# Dummy data definitions
CATEGORY_DATA = [
    {"name": "Electronics", "description": "Devices, gadgets, and appliances"},
    {"name": "Books", "description": "Fiction, non-fiction, academic books"},
    {"name": "Clothing", "description": "Men's and Women's clothing"},
    {"name": "Home Decor", "description": "Furniture and decorative items"},
    {"name": "Fitness", "description": "Gym equipment and accessories"},
    {"name": "Toys", "description": "Kids' toys, puzzles, and games"},
]


REVIEW_TEXTS = [
    "Excellent quality, highly recommended!",
    "Could be better, but overall satisfied.",
    "Very poor experience, won't recommend.",
    "Amazing product, value for money!",
    "Not worth the price, disappointed.",
    "Super fast delivery and great customer service.",
    "The product exceeded my expectations, very happy!",
    "Build quality is decent, but could be improved.",
    "Had some issues initially, but customer support helped.",
    "Not satisfied, the product doesn't match the description.",
    "Highly durable and well-made, loved it!",
    "A must-buy for anyone looking for this category.",
    "Color and design are as shown in the images, very nice.",
    "Performance is fantastic, runs smoothly without issues.",
    "Packing was poor, arrived with minor damages.",
    "Affordable and does the job well, good budget option.",
    "Quality is top-notch, worth every penny spent.",
    "Received a defective piece, but got a replacement quickly.",
    "Disappointed with the durability, broke within a month.",
    "The product has some great features but also some drawbacks.",
    "Installation was quick and easy, instructions were clear.",
    "Overpriced for the quality offered, wouldn't recommend.",
    "Superb product, would definitely purchase again.",
    "User-friendly and easy to operate, great for beginners.",
    "Delivery took longer than expected, but the product is good.",
]


TONES = ["Positive", "Neutral", "Negative"]
SENTIMENTS = ["Happy", "Okay", "Unhappy"]

# Function to insert categories


def create_categories(db: Session):
    existing_categories = db.query(Category).count()
    if existing_categories == 0:
        for category in CATEGORY_DATA:
            new_category = Category(
                name=category["name"], description=category["description"])
            db.add(new_category)
        db.commit()
        print("Categories added successfully!")
    else:
        print("Categories already exist, skipping insertion.")

# Function to insert review history


def create_reviews(db: Session):
    categories = db.query(Category).all()
    if not categories:
        print("No categories found. Insert categories first.")
        return

    for i in range(50):  # Generate 50 dummy reviews
        category = random.choice(categories)
        review_id = f"rev_{random.randint(1, 30)}"
        created_at = datetime.now() - timedelta(days=random.randint(1, 365))
        updated_at = created_at + timedelta(days=random.randint(1, 10))

        review = ReviewHistory(
            text=random.choice(REVIEW_TEXTS),
            stars=random.randint(1, 10),
            review_id=review_id,
            tone=random.choice(TONES) if random.choice(
                [True, False]) else None,
            sentiment=random.choice(SENTIMENTS) if random.choice(
                [True, False]) else None,
            category_id=category.id,
            created_at=created_at,
            updated_at=updated_at,
        )
        db.add(review)

    db.commit()
    print("Dummy review data added successfully!")

# Main function to insert data


def load_dummy_data():
    with get_db() as db:
        try:
            create_categories(db)
            create_reviews(db)
        finally:
            pass


if __name__ == "__main__":
    load_dummy_data()
