from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.rest.dependencies import get_current_user, get_db_session
from src.core.services.authentication_service import (
    AuthenticationService,
)
from src.core.services.password_reset_service import (
    PasswordResetService,
)
from src.data.models.postgres.users import User
from src.schemas.authentication_schema import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    LoginResponse,
    MessageResponse,
    RefreshResponse,
    RefreshTokenRequest,
    ResetPasswordRequest,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(
        get_db_session,
    ),
) -> dict[str, str]:
    auth_service = AuthenticationService(
        db,
    )

    return await auth_service.login(
        username=form_data.username,
        password=form_data.password,
    )


@router.post(
    "/refresh",
    response_model=RefreshResponse,
)
async def refresh_access_token(
    payload: RefreshTokenRequest,
    db: AsyncSession = Depends(
        get_db_session,
    ),
) -> dict[str, str]:
    auth_service = AuthenticationService(
        db,
    )

    return await auth_service.refresh_access_token(
        payload.refresh_token,
    )


@router.post(
    "/logout",
)
async def logout(
    payload: RefreshTokenRequest,
    db: AsyncSession = Depends(
        get_db_session,
    ),
) -> dict[str, str]:
    auth_service = AuthenticationService(
        db,
    )

    return await auth_service.logout(
        payload.refresh_token,
    )


@router.post(
    "/forgot-password",
    response_model=MessageResponse,
)
async def forgot_password(
    payload: ForgotPasswordRequest,
    db: AsyncSession = Depends(
        get_db_session,
    ),
) -> dict[str, str]:
    service = PasswordResetService(
        db,
    )

    return await service.request_password_reset(
        payload.email,
    )


@router.post(
    "/reset-password",
    response_model=MessageResponse,
)
async def reset_password(
    payload: ResetPasswordRequest,
    db: AsyncSession = Depends(
        get_db_session,
    ),
) -> dict[str, str]:
    service = PasswordResetService(
        db,
    )

    return await service.reset_password(
        token=payload.token,
        new_password=payload.new_password,
    )


@router.post(
    "/change-password",
)
async def change_password(
    payload: ChangePasswordRequest,
    current_user: User = Depends(
        get_current_user,
    ),
    db: AsyncSession = Depends(
        get_db_session,
    ),
) -> dict[str, str]:
    auth_service = AuthenticationService(
        db,
    )

    return await auth_service.change_password(
        current_user=current_user,
        payload=payload,
    )
