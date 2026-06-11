from typing import cast
from uuid import UUID

from sqlalchemy import select

from src.data.models.postgres.enums import UserRole
from src.data.models.postgres.users import User
from src.data.repositories.base_repo import BaseRepository


class UserRepository(BaseRepository):
    async def get_user_by_email(
        self,
        email: str,
    ) -> User | None:
        stmt = select(User).where(
            User.email == email,
        )

        result = await self.execute(stmt)

        return cast(User | None, result.scalar_one_or_none())

    async def get_user_by_id(
        self,
        user_id: UUID,
    ) -> User | None:
        stmt = select(User).where(
            User.id == user_id,
        )

        result = await self.execute(stmt)

        return cast(User | None, result.scalar_one_or_none())

    async def update_password(
        self,
        user: User,
        password_hash: str,
    ) -> None:
        user.password_hash = password_hash

        await self.session.flush()

    async def create_user(
        self,
        user: User,
    ) -> User:
        self.session.add(user)

        await self.session.flush()

        await self.session.refresh(user)

        return user

    async def get_users(
        self,
        role: UserRole | None = None,
        allowed_roles: tuple[UserRole, ...] | None = None,
    ) -> list[User]:
        stmt = select(User)

        if role is not None:
            stmt = stmt.where(
                User.role == role,
            )

        elif allowed_roles is not None:
            stmt = stmt.where(
                User.role.in_(allowed_roles),
            )

        result = await self.execute(stmt)

        return cast(list[User], list(result.scalars().all()))

    async def update_user_status(
        self,
        user_id: UUID,
        is_active: bool,
    ) -> User | None:
        user = await self.get_user_by_id(
            user_id,
        )

        if not user:
            return None

        user.is_active = is_active

        await self.session.flush()

        return user
