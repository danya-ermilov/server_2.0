from fastapi import HTTPException
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.auth.hashing import get_password_hash
from app.models.user import User as modelUser
from app.models.xp_history import XpHistory as modelXpHistory
from app.models.user_stat import UserStat as modelUserStat
from app.schemas.users import UserUpdate, UserStat
from app.crud import products as crud_product
from app.models.user import User


async def get_user(db: AsyncSession, username: str) -> modelUser | None:
    result = await db.execute(select(modelUser).where(modelUser.username == username))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_user_with_xp(db: AsyncSession, username: str):
    query = text(
        """
        SELECT
            u.id AS user_id,
            u.username,
            h.product_id,
            COALESCE(SUM(h.points), 0) AS total_points,
            us.total_xp,
            us.skill_mind,
            us.skill_social,
            us.skill_sport
        FROM users AS u
        LEFT JOIN user_stats AS us ON u.id = us.user_id
        LEFT JOIN xp_history AS h ON u.id = h.user_id
        WHERE u.username = :username
        GROUP BY
            u.id, u.username, h.product_id,
            us.total_xp, us.skill_mind, us.skill_social, us.skill_sport
        ORDER BY h.product_id;
    """
    )

    result = await db.execute(query, {"username": username})
    rows = result.fetchall()
    r = rows[0]
    activities = [
        {
            "user_id": r.user_id,
            "username": r.username,
            "total_xp": r.total_xp,
            "skill_mind": r.skill_mind,
            "skill_social": r.skill_social,
            "skill_sport": r.skill_sport,
        }
    ]

    if not rows:
        raise HTTPException(status_code=404, detail="User not found or no XP history")

    for r in rows:
        product = await crud_product.get_product(db, r.product_id)
        activities.append(
            {
                "product": product.name,
                "total_points": r.total_points,
            }
        )

    return activities


async def create_user(db: AsyncSession, username: str, password: str) -> modelUser:
    hashed_pw = get_password_hash(password)
    new_user = modelUser(username=username, password_hash=hashed_pw)
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except IntegrityError:
        await db.rollback()
        raise


async def update_user(
    db: AsyncSession, username: str, payload: UserUpdate
) -> modelUser:
    user = await get_user(db, username)
    for field, value in payload.model_dump(exclude_unset=True).items():
        if value is not None:
            if field == "password":
                field = "password_hash"
                value = get_password_hash(value)
            setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, username: str):
    user = await get_user(db, username)
    await db.delete(user)
    await db.commit()


async def get_user_stat(db: AsyncSession, username: str) -> UserStat:
    user = await get_user(db, username)
    result = await db.execute(
        select(modelUserStat).where(modelUserStat.user_id == user.id)
    )
    user_stat = result.scalar_one_or_none()
    if not user_stat:
        db.add(
            modelUserStat(
                user_id=user.id,
            )
        )
        await db.commit()

    return user_stat


async def update_user_stat(db: AsyncSession, username: str, xp: int, tag: str):
    user_stat = await get_user_stat(db, username)

    setattr(user_stat, tag, getattr(user_stat, tag, 0) + xp // 10)

    user_stat.total_xp += xp // 10

    db.add(user_stat)
    await db.commit()
    await db.refresh(user_stat)

    return user_stat


async def set_user_xp(
    db: AsyncSession, username: str, product_id: int, current_user: User
):
    user = await get_user(db, username)
    product = await crud_product.get_product(db, product_id)

    if product.owner_id != current_user.id and current_user.role != "admin":
        return None

    xp_record = modelXpHistory(
        user_id=user.id,
        product_id=product_id,
        category=product.tag_name,
        points=product.xp,
        created_at=datetime.utcnow(),
    )
    db.add(xp_record)

    await update_user_stat(db, username, product.xp, product.tag_name)

    await db.commit()
    await db.refresh(xp_record)

    return xp_record
