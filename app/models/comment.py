from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, func
from app.db.database import Base
from sqlalchemy.orm import relationship


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    author = relationship("User", back_populates="comments")
    product = relationship("Product", back_populates="comments", passive_deletes=True)
