from sqlalchemy import Column, Integer, String
from app.db.database import Base
from sqlalchemy.orm import relationship


class Tag(Base):
    __tablename__ = "tags"

    name = Column(String, primary_key=True, nullable=False, unique=True, index=True)

    products = relationship("Product", back_populates="tag", cascade="all, delete")
