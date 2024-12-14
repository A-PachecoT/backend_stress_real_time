from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.auth import UserResponse
from app.schemas.user import UserProfileCreate, UserProfileUpdate

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update user profile information"""
    # Update only provided fields
    for field, value in profile_data.dict(exclude_unset=True).items():
        setattr(current_user, field, value)

    await db.commit()
    await db.refresh(current_user)

    return current_user


@router.post("/profile", response_model=UserResponse)
async def create_profile(
    profile_data: UserProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    for field, value in profile_data.model_dump().items():
        setattr(current_user, field, value)

    await db.commit()
    await db.refresh(current_user)
    return current_user
