from collections.abc import AsyncGenerator, Awaitable, Callable
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security.jwt_provider import jwt_provider
from src.data.clients.postgres_client import get_session_factory
from src.data.models.postgres.enums import UserRole
from src.data.models.postgres.users import User
from src.data.repositories.user_repo import UserRepository

# =========================
# Database Dependency
# =========================


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    session_factory = get_session_factory()

    async with session_factory() as session:
        try:
            yield session

            await session.commit()

        except Exception:
            await session.rollback()
            raise


# =========================
# JWT Security
# =========================

security = HTTPBearer()


# =========================
# Current User
# =========================


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security,
    ),
    session: AsyncSession = Depends(
        get_db_session,
    ),
) -> User:
    token = credentials.credentials

    try:
        payload = jwt_provider.decode_token(
            token,
        )

    except Exception as err:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        ) from err

    if payload.get("token_type") != "access":
        raise HTTPException(
            status_code=401,
            detail="Invalid token type",
        )

    repo = UserRepository(session)

    user = await repo.get_user_by_id(
        UUID(payload["sub"]),
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User is inactive",
        )

    return user


def require_roles(
    *allowed_roles: UserRole,
) -> Callable[..., Awaitable[User]]:
    async def role_checker(
        current_user: User = Depends(
            get_current_user,
        ),
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions",
            )

        return current_user

    return role_checker
