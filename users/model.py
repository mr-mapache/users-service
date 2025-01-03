from uuid import UUID
from typing import Optional
from dataclasses import dataclass
from users.ports import Users, Emails, Accounts

@dataclass
class User:
    id: UUID
    username: Optional[str]
    emails: Emails
    accounts: Accounts

@dataclass
class Repository:
    users: Users