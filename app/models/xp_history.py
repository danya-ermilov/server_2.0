from datetime import datetime
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime
from app.db.database import Base
from sqlalchemy.orm import relationship


class XpHistory(Base):
    __tablename__ = "xp_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    category = Column(String)
    points = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="xp_records")
