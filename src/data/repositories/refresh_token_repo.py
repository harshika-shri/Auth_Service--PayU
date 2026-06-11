from typing import cast
from uuid import UUID

from sqlalchemy import select

from src.data.models.postgres.refresh_tokens import RefreshToken
from src.data.repositories.base_repo import BaseRepository


class RefreshTokenRepository(BaseRepository):
    async def create_refresh_token(
        self,
        refresh_token: RefreshToken,
    ) -> RefreshToken:
        self.session.add(
            refresh_token,
        )

        await self.session.flush()

        return refresh_token

    async def get_refresh_token_by_jti(
        self,
        token_jti: str,
    ) -> RefreshToken | None:
        stmt = select(
            RefreshToken,
        ).where(
            RefreshToken.token_jti == token_jti,
        )

        result = await self.execute(
            stmt,
        )

        return cast(RefreshToken | None, result.scalar_one_or_none())

    async def revoke_refresh_token(
        self,
        token_jti: str,
    ) -> RefreshToken | None:
        token = await self.get_refresh_token_by_jti(
            token_jti,
        )

        if token:
            token.is_revoked = True

            await self.session.flush()

        return token

    async def revoke_all_user_refresh_tokens(
        self,
        user_id: UUID,
    ) -> None:
        stmt = select(
            RefreshToken,
        ).where(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked.is_(False),
        )

        result = await self.execute(
            stmt,
        )

        tokens = cast(list[RefreshToken], list(result.scalars().all()))

        for token in tokens:
            token.is_revoked = True

        await self.session.flush()
