from datetime import datetime, timedelta, timezone
from typing import Annotated, List

import jwt
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.db.database import get_db
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas.users import (
    TokenData,
    User,
    UserInDB,
    UserCreate,
    UserUpdate
)
from app.models.user import User as modelUser

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ----------------------------------
# Password helpers
# ----------------------------------


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# ----------------------------------
# Get user by username (ORM)
# ----------------------------------


async def get_user(db: AsyncSession, username: str) -> modelUser | None:
    result = await db.execute(select(modelUser).where(modelUser.username == username))
    return result.scalar_one_or_none()

# ----------------------------------
# Create JWT token
# ----------------------------------


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ----------------------------------
# Auth dependencies
# ----------------------------------


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db)
) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user = await get_user(db, token_data.username)
    if not user:
        raise credentials_exception

    return UserInDB.from_orm(user)


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# ----------------------------------
# Paths
# ----------------------------------


@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    hashed_pw = get_password_hash(user.password)
    new_user = modelUser(username=user.username, password_hash=hashed_pw)
    db.add(new_user)
    try:
        await db.commit()
        return {"message": "User registered successfully"}
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Username already exists")


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@router.get("/users/getall", response_model=List[UserInDB])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(modelUser))
    users = result.scalars().all()
    return users


@router.get("/users/getone/{username}", response_model=UserInDB)
async def get_one_users(username: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(modelUser).where(modelUser.username == username))
    users = result.scalar_one_or_none()
    return users


@router.delete("/users/delete/{username}")
async def delete_user(
    username: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.username == username or current_user.role == 'admin':
        result = await db.execute(select(modelUser).where(modelUser.username == username))
        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        await db.delete(user)
        await db.commit()
    else:
        HTTPException(status_code=404, detail='Access denied')


@router.put("/update/{username}", response_model=UserInDB)
async def update_user(
    username: str,
    payload: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.username == username or current_user.role == 'admin':
        result = await db.execute(select(modelUser).where(modelUser.id == current_user.id))
        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        if payload.username:
            user.username = payload.username
        if payload.password:
            user.password_hash = get_password_hash(payload.password)
        if payload.role:
            user.role = payload.role

        await db.commit()
        await db.refresh(user)

        return user
    else:
        HTTPException(status_code=404, detail='Access denied')
