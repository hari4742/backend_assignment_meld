from sqlalchemy import Column, BigInteger, String, DateTime, Integer
from sqlalchemy.sql import func
from app.db.session import Base


class AccessLog(Base):
    __tablename__ = "access_log"

    id = Column(BigInteger().with_variant(Integer, "sqlite"),
                primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
