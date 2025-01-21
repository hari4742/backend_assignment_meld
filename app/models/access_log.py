from sqlalchemy import Column, BigInteger, String
from app.db.session import Base


class AccessLog(Base):
    __tablename__ = "access_log"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
