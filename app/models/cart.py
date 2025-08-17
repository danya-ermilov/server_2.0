from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.database import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))

    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="unique_cart_item"),
    )

    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items", lazy="selectin")
