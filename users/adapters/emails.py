from typing import Optional
from typing import override

from sqlalchemy.sql import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from users.ports import Emails as Collection
from users.schemas import Email
from users.adapters.schemas import emails

class Emails(Collection):
    def __init__(self, session: AsyncSession, user_pk: int):
        self.session = session
        self.user_pk = user_pk

    @override
    async def add(self, email: Email):
        if email.is_primary:
            command = (
                update(emails)
                .where(
                    emails.columns.user_pk == self.user_pk,
                    emails.columns.email_is_primary == True
                )
                .values(email_is_primary=False)
            )
            await self.session.execute(command)
            
        command = (
            insert(emails).
            values(
                email_address=email.address,
                email_is_primary=email.is_primary,
                email_is_verified=email.is_verified,                
                user_pk=self.user_pk
            ).
            returning(emails.columns.pk)
        )
        result = await self.session.execute(command)
        email.pk = result.scalar()

    @override
    async def get(self, address: str) -> Optional[Email]:
        query = (
            select(emails).
            where(
                emails.columns.user_pk == self.user_pk,
                emails.columns.email_address == address
            )
        )
        result = await self.session.execute(query)
        row = result.fetchone()
        if not row:
            return None
        return Email(address=row.email_address, is_primary=row.email_is_primary, is_verified=row.email_is_verified, pk=row.pk)
    
    @override
    async def list(self) -> list[Email]:
        query = (
            select(emails).
            where(emails.columns.user_pk == self.user_pk)
        )
        result = await self.session.execute(query)
        rows = result.fetchall()
        return [Email(address=row.email_address, is_primary=row.email_is_primary, is_verified=row.email_is_verified, pk=row.pk) for row in rows]

    @override
    async def update(self, email: Email):
        if email.is_primary:
            command = (
                update(emails)
                .where(
                    emails.columns.user_pk == self.user_pk,
                    emails.columns.email_is_primary == True
                )
                .values(email_is_primary=False)
            )
            await self.session.execute(command)
            
        command = (
            update(emails)
            .where(emails.columns.email_address == email.address)
            .values(email_is_primary=email.is_primary, email_is_verified=email.is_verified)
        )
        await self.session.execute(command)

    @override
    async def remove(self, email: Email):
        command = (
            delete(emails).where(
                emails.columns.user_pk == self.user_pk,
                emails.columns.email_address == email.address
            )
        )
        await self.session.execute(command)