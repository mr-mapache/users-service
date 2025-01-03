from uuid import UUID
from datetime import datetime
from datetime import timezone
from typing import Optional
from typing import Any
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

class Schema(BaseModel):
    pk: Optional[int] = Field(default=None, exclude=True)

class User(Schema):
    id: UUID
    username: Optional[str]

class Account(Schema):
    id: str
    type: str
    provider: str

class Email(Schema):
    address: EmailStr
    is_primary: bool
    is_verified: bool

class Session(Schema):
    id: UUID
    payload: dict[str, Any]
    expires_at: datetime