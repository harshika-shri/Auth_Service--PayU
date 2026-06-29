import logging
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.settings import settings
from src.core.security.jwt_provider import jwt_provider
from src.core.services.sendgrid_service import SendGridService
from src.data.repositories.refresh_token_repo import (
    RefreshTokenRepository,
)
from src.data.repositories.user_repo import UserRepository
from src.utils.password import hash_password

logger = logging.getLogger(__name__)


class PasswordResetService:
    GENERIC_SUCCESS_MESSAGE = (
        "If an account exists for that email, a password reset link has been sent."
    )

    def __init__(self, session: AsyncSession) -> None:
        self.user_repo = UserRepository(session)
        self.refresh_repo = RefreshTokenRepository(session)
        self.sendgrid_service = SendGridService()

    async def request_password_reset(
        self,
        email: str,
    ) -> dict[str, str]:
        user = await self.user_repo.get_user_by_email(email)

        if user is None or not user.is_active:
            return {"message": self.GENERIC_SUCCESS_MESSAGE}

        raw_token = jwt_provider.create_password_reset_token(
            user_id=str(user.id),
        )

        reset_url = (
            f"{settings.FRONTEND_URL.rstrip('/')}/reset-password?token={raw_token}"
        )
        html_content = (
            f"<p>Hello {user.name},</p>"
            "<p>We received a request to reset your PayU Finance password.</p>"
            f'<p><a href="{reset_url}">Set a new password</a></p>'
            "<p>This link expires in "
            f"{settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES} minutes.</p>"
            "<p>If you did not request this, you can ignore this email.</p>"
        )

        try:
            self.sendgrid_service.send_email(
                to_email=user.email,
                subject="Reset your PayU Finance password",
                html_content=html_content,
            )
        except Exception:
            logger.exception(
                "Failed to send password reset email for user_id=%s",
                user.id,
            )

        return {"message": self.GENERIC_SUCCESS_MESSAGE}

    async def reset_password(
        self,
        token: str,
        new_password: str,
    ) -> dict[str, str]:
        try:
            payload = jwt_provider.decode_token(token)
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired password reset link.",
            ) from err

        if payload.get("token_type") != "password_reset":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired password reset link.",
            )

        user = await self.user_repo.get_user_by_id(
            UUID(payload["sub"]),
        )

        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired password reset link.",
            )

        await self.user_repo.update_password(
            user=user,
            password_hash=hash_password(new_password),
        )
        await self.refresh_repo.revoke_all_user_refresh_tokens(user.id)

        return {"message": "Password has been reset successfully."}
