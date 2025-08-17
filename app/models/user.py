from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)
    role = Column(String, default='user')

    products = relationship("Product", back_populates="owner", cascade="all, delete")
    cart_items = relationship("CartItem", back_populates="user", cascade="all, delete")
