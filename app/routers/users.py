from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_active_user
from app.auth.hashing import verify_password
from app.auth.jwt_handler import create_access_token
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.crud import users as crud_user
from app.db.database import get_db
from app.models.user import User as modelUser
from app.schemas.users import User, UserCreate, UserInDB, UserUpdate

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
        {"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
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
