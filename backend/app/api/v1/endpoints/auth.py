import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.deps import get_db, get_current_active_user
from app.core.config import settings
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.db.models.user import User
from app.db.models.user_profile import UserProfile
from app.domain.schemas.auth import (
    UserRegister,
    UserLogin,
    TokenResponse,
    RefreshTokenRequest,
)
from app.domain.schemas.user import UserResponse

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserRegister,
    db: AsyncSession = Depends(get_db),
) -> Any:
    # Check duplicate email
    result = await db.execute(select(User).where(User.email == user_in.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "data": None,
                "error": {
                    "code": "DUPLICATE_EMAIL",
                    "message": "User with this email already exists",
                    "details": [],
                },
            },
        )

    # Create User
    hashed_password = get_password_hash(user_in.password)
    new_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        role="user",
        is_active=True,
    )
    db.add(new_user)
    await db.flush()

    # Create Profile
    new_profile = UserProfile(
        user_id=new_user.id,
        full_name=user_in.full_name,
    )
    db.add(new_profile)
    await db.commit()

    # Re-query user with profile loaded
    result = await db.execute(
        select(User).options(selectinload(User.profile)).where(User.id == new_user.id)
    )
    created_user = result.scalar_one()

    access_token = create_access_token(created_user.id)
    refresh_token = create_refresh_token(created_user.id)

    return {
        "success": True,
        "data": {
            "user": UserResponse.model_validate(created_user),
            "tokens": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            },
        },
        "error": None,
    }


@router.post("/login")
async def login(
    user_in: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> Any:
    result = await db.execute(
        select(User).options(selectinload(User.profile)).where(User.email == user_in.email)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "data": None,
                "error": {
                    "code": "INVALID_CREDENTIALS",
                    "message": "Invalid email or password",
                    "details": [],
                },
            },
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "data": None,
                "error": {
                    "code": "INACTIVE_USER",
                    "message": "User account is disabled",
                    "details": [],
                },
            },
        )

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return {
        "success": True,
        "data": {
            "user": UserResponse.model_validate(user),
            "tokens": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            },
        },
        "error": None,
    }


@router.post("/refresh")
async def refresh_token(
    refresh_in: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
) -> Any:
    payload = decode_token(refresh_in.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "data": None,
                "error": {
                    "code": "INVALID_REFRESH_TOKEN",
                    "message": "Invalid or expired refresh token",
                    "details": [],
                },
            },
        )

    user_id_str = payload.get("sub")
    try:
        user_uuid = uuid.UUID(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "data": None,
                "error": {
                    "code": "INVALID_REFRESH_TOKEN",
                    "message": "Invalid token subject",
                    "details": [],
                },
            },
        )

    result = await db.execute(select(User).where(User.id == user_uuid))
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "data": None,
                "error": {
                    "code": "USER_NOT_FOUND",
                    "message": "User inactive or no longer exists",
                    "details": [],
                },
            },
        )

    new_access_token = create_access_token(user.id)
    new_refresh_token = create_refresh_token(user.id)

    return {
        "success": True,
        "data": {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        },
        "error": None,
    }


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    return {
        "success": True,
        "data": {"message": "Successfully logged out"},
        "error": None,
    }


@router.get("/me")
async def read_current_user(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    return {
        "success": True,
        "data": UserResponse.model_validate(current_user),
        "error": None,
    }
