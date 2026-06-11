from uuid import UUID, uuid4

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models.postgres.enums import UserRole
from src.data.models.postgres.users import User
from src.data.repositories.refresh_token_repo import (
    RefreshTokenRepository,
)
from src.data.repositories.user_repo import UserRepository
from src.schemas.user_schema import (
    CreateUserRequest,
    UserResponse,
)
from src.utils.password import hash_password

ADMIN_VISIBLE_ROLES: tuple[UserRole, ...] = (
    UserRole.FINANCE_ASSOCIATE,
    UserRole.FINANCE_MANAGER,
)


class UserService:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.user_repo = UserRepository(session)
        self.refresh_repo = RefreshTokenRepository(session)

    async def create_user(
        self,
        current_user: User,
        payload: CreateUserRequest,
    ) -> UserResponse:
        if payload.role == UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Admin users cannot be created",
            )

        existing_user = await self.user_repo.get_user_by_email(
            payload.email,
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists",
            )

        user = User(
            id=uuid4(),
            company_id=current_user.company_id,
            name=payload.name,
            email=payload.email,
            password_hash=hash_password(
                payload.password,
            ),
            role=payload.role,
            is_active=True,
        )

        created_user = await self.user_repo.create_user(
            user,
        )

        return UserResponse.model_validate(
            created_user,
        )

    async def get_users(
        self,
        current_user: User,
        role: UserRole | None = None,
    ) -> list[UserResponse]:
        if current_user.role == UserRole.ADMIN:
            if role in ADMIN_VISIBLE_ROLES:
                users = await self.user_repo.get_users(
                    role=role,
                )

            elif role is None:
                users = await self.user_repo.get_users(
                    allowed_roles=ADMIN_VISIBLE_ROLES,
                )

            else:
                users = []

            return [
                UserResponse.model_validate(
                    user,
                )
                for user in users
            ]

        users = await self.user_repo.get_users(
            role,
        )

        return [
            UserResponse.model_validate(
                user,
            )
            for user in users
        ]

    async def update_user_status(
        self,
        user_id: UUID,
        is_active: bool,
    ) -> dict[str, str]:
        user = await self.user_repo.get_user_by_id(
            user_id,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if user.role == UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin user cannot be modified",
            )

        await self.user_repo.update_user_status(
            user_id=user_id,
            is_active=is_active,
        )

        if not is_active:
            await self.refresh_repo.revoke_all_user_refresh_tokens(
                user_id,
            )

        return {
            "message": (
                "User activated successfully"
                if is_active
                else "User deactivated successfully"
            )
        }
