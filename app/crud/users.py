from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.hashing import get_password_hash
from app.models.user import User as modelUser
from app.schemas.users import UserUpdate


async def get_user(db: AsyncSession, username: str) -> modelUser | None:
    result = await db.execute(select(modelUser).where(modelUser.username == username))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


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
