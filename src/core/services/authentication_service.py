from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security.jwt_provider import jwt_provider
from src.data.models.postgres.refresh_tokens import RefreshToken
from src.data.models.postgres.users import User
from src.data.repositories.refresh_token_repo import (
    RefreshTokenRepository,
)
from src.data.repositories.user_repo import UserRepository
from src.schemas.authentication_schema import (
    ChangePasswordRequest,
)
from src.utils.password import (
    hash_password,
    verify_password,
)


class AuthenticationService:
    def __init__(self, session: AsyncSession) -> None:
        self.user_repo = UserRepository(session)
        self.refresh_repo = RefreshTokenRepository(session)

    async def login(
        self,
        username: str,
        password: str,
    ) -> dict[str, str]:
        user = await self.user_repo.get_user_by_email(
            username,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        access_token = jwt_provider.create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        (
            refresh_token,
            token_jti,
            expires_at,
        ) = jwt_provider.create_refresh_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        await self.refresh_repo.create_refresh_token(
            RefreshToken(
                user_id=user.id,
                token_jti=token_jti,
                expires_at=expires_at,
            )
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def change_password(
        self,
        current_user: User,
        payload: ChangePasswordRequest,
    ) -> dict[str, str]:
        if not verify_password(
            payload.old_password,
            current_user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Old password is incorrect",
            )

        password_hash = hash_password(
            payload.new_password,
        )

        await self.user_repo.update_password(
            user=current_user,
            password_hash=password_hash,
        )

        return {
            "message": "Password changed successfully",
        }

    async def refresh_access_token(
        self,
        refresh_token: str,
    ) -> dict[str, str]:
        try:
            payload = jwt_provider.decode_token(
                refresh_token,
            )

        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            ) from err

        if payload["token_type"] != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

        token_record = await self.refresh_repo.get_refresh_token_by_jti(
            payload["jti"],
        )

        if not token_record:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token not found",
            )

        if token_record.is_revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token revoked",
            )

        user = await self.user_repo.get_user_by_id(
            UUID(payload["sub"]),
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        access_token = jwt_provider.create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    async def logout(
        self,
        refresh_token: str,
    ) -> dict[str, str]:
        try:
            payload = jwt_provider.decode_token(
                refresh_token,
            )

        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            ) from err

        if payload["token_type"] != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

        await self.refresh_repo.revoke_refresh_token(
            payload["jti"],
        )

        return {
            "message": "Logged out successfully",
        }
