from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func
from app.db.session import Base


class AccessLog(Base):
    __tablename__ = "access_log"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
