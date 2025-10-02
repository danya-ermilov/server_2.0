from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_active_user
from app.auth.hashing import verify_password
from app.auth.jwt_handler import create_access_token
from app.core.config import settings
from app.crud import users as crud_user
from app.db.database import get_db
from app.models.user import User as modelUser
from app.schemas.users import User, UserCreate, UserInDB, UserUpdate

from app.auth.dependencies import get_current_user

router = APIRouter()


@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        await crud_user.create_user(db, user.username, user.password)
        return {"message": "User registered successfully"}
    except Exception:
        raise HTTPException(status_code=400, detail="Username already exists")


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await crud_user.get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        {"sub": user.username}, timedelta(minutes=settings.access_token_expire_minutes)
    )
    return {"access_token": token, "token_type": "bearer"}


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/users/getall", response_model=List[UserInDB])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(modelUser))
    return result.scalars().all()


@router.get("/users/getone/{username}", response_model=UserInDB)
async def get_one_user(username: str, db: AsyncSession = Depends(get_db)):
    user = await crud_user.get_user(db, username)
    return user


@router.get("/users/getone/{username}/xp")
async def get_one_user_with_xp(username: str, db: AsyncSession = Depends(get_db)):
    user = await crud_user.get_user_with_xp(db, username)
    return user


@router.delete("/users/delete/")
async def delete_user(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    await crud_user.delete_user(db, current_user.username)
    return {"message": "User deleted"}


@router.put("/users/update/", response_model=UserInDB)
async def update_user(
    payload: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await crud_user.update_user(db, current_user.username, payload)


@router.post("/users/set_xp")
async def set_xp_bulk(
    usernames: str = Body(..., example="user1 user2"),
    product_id: int = Body(..., example=123),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    results = []

    usernames_list: List[str] = [
        u.strip() for u in usernames.replace(",", " ").split() if u.strip()
    ]

    if not usernames_list:
        raise HTTPException(
            status_code=400, detail="Список пользователей пуст или некорректен"
        )

    for username in usernames_list:
        try:
            xp_record = await crud_user.set_user_xp(
                db=db,
                username=username,
                product_id=product_id,
                current_user=current_user,
            )

            stats = await crud_user.get_user_stat(db, username)

            results.append(
                {
                    "message": "XP успешно начислены",
                    "user": {
                        "username": username,
                    },
                    "xp_record": {
                        "product_id": xp_record.product_id,
                        "category": xp_record.category,
                        "points": xp_record.points,
                        "created_at": xp_record.created_at,
                    },
                    "updated_stats": {
                        "total_xp": stats.total_xp,
                        "skill_mind": stats.skill_mind,
                        "skill_social": stats.skill_social,
                        "skill_sport": stats.skill_sport,
                    },
                }
            )
        except HTTPException as e:
            results.append({"username": username, "error": e.detail})
    return {"message": "XP начислены", "results": results}
