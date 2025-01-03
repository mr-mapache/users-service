from uuid import UUID
from typing import Optional
from typing import override

from sqlalchemy.sql import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from users.ports import Accounts as Collection
from users.schemas import Account
from users.adapters.schemas import accounts

class Accounts(Collection):
    def __init__(self, session: AsyncSession, user_pk: int):
        self.session = session
        self.user_pk = user_pk

    @override
    async def add(self, account: Account):
        command = (
            insert(accounts).
            values(
                account_id=account.id,
                account_type=account.type,
                account_provider=account.provider,
                user_pk=self.user_pk
            ).
            returning(accounts.columns.pk)
        )
        result = await self.session.execute(command)
        account.pk = result.scalar()

    @override
    async def get(self, provider: str, id: str) -> Optional[Account]:
        query = (
            select(accounts).
            where(
                accounts.columns.user_pk == self.user_pk,
                accounts.columns.account_provider == provider,
                accounts.columns.account_id == id
            )
        )
        result = await self.session.execute(query)
        row = result.fetchone()
        if not row:
            return None
        return Account(id=row.account_id, type=row.account_type, provider=row.account_provider, pk=row.pk)

    @override
    async def remove(self, account: Account):
        command = (
            delete(accounts).where(
                accounts.columns.user_pk == self.user_pk,
                accounts.columns.account_provider == account.provider,
                accounts.columns.account_id == account.id
            )
        )
        await self.session.execute(command)