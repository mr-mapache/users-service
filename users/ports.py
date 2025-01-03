from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional
from users.schemas import User, Email, Account, Session

class Users(ABC):

    @abstractmethod
    async def add(self, user: User):...

    @abstractmethod
    async def get(self, id: UUID) -> Optional[User]:...

    @abstractmethod
    async def update(self, user: User):...

    @abstractmethod
    async def remove(self, id: UUID):...


class Accounts(ABC):

    @abstractmethod
    async def add(self, account: Account):...

    @abstractmethod
    async def get(self, provider: str, id: str) -> Optional[Account]:...

    @abstractmethod
    async def remove(self, account: Account):...


class Emails(ABC):

    @abstractmethod
    async def add(self, email: Email):...

    @abstractmethod
    async def get(self, address: str) -> Optional[Email]:...

    @abstractmethod
    async def update(self, email: Email):...

    @abstractmethod
    async def list(self) -> list[Email]:...

    @abstractmethod
    async def remove(self, email: Email):...


class Sessions(ABC):
    
    @abstractmethod
    async def put(self, session: Session):...

    @abstractmethod
    async def get(self, id: UUID) -> Session:...

    @abstractmethod
    async def remove(self, session: Session):...