from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    cart_count = Column(Integer, default=0)

    owner = relationship("User", back_populates="products")
    cart_items = relationship(
        "CartItem", back_populates="product", cascade="all, delete"
    )
    comments = relationship(
        "Comment", back_populates="product", cascade="all, delete-orphan"
    )
