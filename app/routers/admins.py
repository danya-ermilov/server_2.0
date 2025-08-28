from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_active_admin_user
from app.crud import users as crud_user, tags as crud_tag
from app.db.database import get_db
from app.schemas.users import UserUpdate


router = APIRouter(prefix="/admin", tags=["Admin_panel"])


@router.delete(
    "/users/delete/{username}", dependencies=[Depends(get_current_active_admin_user)]
)
async def delete_user(username: str, db: AsyncSession = Depends(get_db)):
    await crud_user.delete_user(db, username)
    return {"message": f"{username} deleted"}


@router.put(
    "/users/update/{username}", dependencies=[Depends(get_current_active_admin_user)]
)
async def update_user(
    payload: UserUpdate, username: str, db: AsyncSession = Depends(get_db)
):
    return await crud_user.update_user(db, username, payload)


@router.post("/tags/create", dependencies=[Depends(get_current_active_admin_user)])
async def create_tag(name: str, db: AsyncSession = Depends(get_db)):
    return await crud_tag.add_tag(db, name)
