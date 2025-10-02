from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import TSVECTOR
from app.db.database import Base
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    tag_name = Column(String, ForeignKey("tags.name", ondelete="CASCADE"))
    cart_count = Column(Integer, default=0)
    xp = Column(Integer, nullable=False)

    search_vector = Column(TSVECTOR)

    owner = relationship("User", back_populates="products")
    tag = relationship("Tag", back_populates="products")
    cart_items = relationship(
        "CartItem", back_populates="product", cascade="all, delete"
    )
    comments = relationship(
        "Comment", back_populates="product", cascade="all, delete-orphan"
    )
