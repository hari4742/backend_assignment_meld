from sqlalchemy import Column, BigInteger, String, Text, Integer
from app.db.session import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(BigInteger().with_variant(Integer, "sqlite"),
                primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)
