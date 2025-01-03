from uuid import UUID
from typing import Optional
from typing import override

from sqlalchemy.sql import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from users.ports import Users as Collection
from users.schemas import User
from users.adapters.schemas import users

class Users(Collection):
    def __init__(self, session: AsyncSession):
        self.session = session

    @override
    async def add(self, user: User):
        command = (
            insert(users).
            values(user_id=user.id, user_username=user.username).
            returning(users.columns.pk)
        )
        result = await self.session.execute(command)
        user.pk = result.scalar()

    @override
    async def get(self, id: UUID) -> Optional[User]:
        query = (
            select(users).
            where(users.columns.user_id == id)
        )
        result = await self.session.execute(query)
        row = result.fetchone()
        if not row:
            return None
        return User(id=row.user_id, username=row.user_username)

    @override
    async def update(self, user: User):
        command = (
            update(users).
            where(users.columns.user_id == user.id).
            values(user_username=user.username)
        )
        await self.session.execute(command)

    @override
    async def remove(self, user: User):
        command = (
            delete(users).
            where(users.columns.user_id == user.id)
        )
        await self.session.execute(command)    