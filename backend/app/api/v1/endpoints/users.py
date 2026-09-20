from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db, get_current_active_user
from app.db.models.user import User
from app.db.models.user_profile import UserProfile
from app.domain.schemas.user import UserProfileResponse, UserProfileUpdate

router = APIRouter()


@router.get("/profile")
async def get_user_profile(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    if not current_user.profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "data": None,
                "error": {
                    "code": "PROFILE_NOT_FOUND",
                    "message": "User profile not found",
                    "details": [],
                },
            },
        )
    return {
        "success": True,
        "data": UserProfileResponse.model_validate(current_user.profile),
        "error": None,
    }


@router.put("/profile")
async def update_user_profile(
    profile_in: UserProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()

    if not profile:
        profile = UserProfile(
            user_id=current_user.id,
            full_name=profile_in.full_name or current_user.email.split("@")[0],
        )
        db.add(profile)

    update_data = profile_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)

    await db.commit()
    await db.refresh(profile)

    return {
        "success": True,
        "data": UserProfileResponse.model_validate(profile),
        "error": None,
    }
