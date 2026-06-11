from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.rest.dependencies import get_db_session, require_roles
from src.core.services.user_service import UserService
from src.data.models.postgres.enums import UserRole
from src.data.models.postgres.users import User
from src.schemas.user_schema import (
    CreateUserRequest,
    UpdateUserStatusRequest,
    UserResponse,
)

router = APIRouter(
    prefix="/users",
    tags=["User Management"],
)


@router.post(
    "",
    response_model=UserResponse,
)
async def create_user(
    payload: CreateUserRequest,
    db: AsyncSession = Depends(
        get_db_session,
    ),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
        ),
    ),
) -> UserResponse:
    user_service = UserService(
        db,
    )

    return await user_service.create_user(
        current_user=current_user,
        payload=payload,
    )


@router.get(
    "",
    response_model=list[UserResponse],
)
async def get_users(
    role: UserRole | None = Query(
        default=None,
    ),
    db: AsyncSession = Depends(
        get_db_session,
    ),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
        ),
    ),
) -> list[UserResponse]:
    user_service = UserService(
        db,
    )

    return await user_service.get_users(
        current_user=current_user,
        role=role,
    )


@router.patch(
    "/{user_id}/status",
)
async def update_user_status(
    user_id: UUID,
    payload: UpdateUserStatusRequest,
    db: AsyncSession = Depends(
        get_db_session,
    ),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
        ),
    ),
) -> dict[str, str]:
    user_service = UserService(
        db,
    )

    return await user_service.update_user_status(
        user_id=user_id,
        is_active=payload.is_active,
    )
