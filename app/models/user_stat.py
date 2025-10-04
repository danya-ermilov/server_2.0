from sqlalchemy import ForeignKey, Column, Integer
from app.db.database import Base
from sqlalchemy.orm import relationship


class UserStat(Base):
    __tablename__ = "user_stats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    total_xp = Column(Integer, default=0)
    skill_mind = Column(Integer, default=0)
    skill_social = Column(Integer, default=0)
    skill_sport = Column(Integer, default=0)
    skill_game = Column(Integer, default=0)

    user = relationship("User", back_populates="stats")
