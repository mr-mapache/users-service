from uuid import UUID
from typing import Optional
from typing import override
from datetime import datetime, timezone, timedelta
from redis.asyncio import Redis
from users.schemas import Session
from users.ports import Sessions as Collection

class Sessions(Collection):
    def __init__(self, user_pk: int, redis: Redis):
        self.user_pk = user_pk
        self.redis = redis
    
    @override
    async def put(self, session: Session):
        expires_in = (session.expires_at - datetime.now(tz=timezone.utc)).total_seconds()
        if expires_in > 0:
            await self.redis.set(str(session.id), str(self.user_pk), ex=expires_in)
            await self.redis.hset('session', str(session.id), mapping=session.payload)

    @override
    async def get(self, id: UUID) -> Optional[Session]:         
        if not await self.redis.get(str(id)):
            return None
        payload = await self.redis.hget('session', str(id))
        expires_in = await self.redis.ttl(str(id))
        expires_at = datetime.now(tz=timezone.utc) + timedelta(seconds=expires_in)
        return Session(id=id, payload=payload, expires_at=expires_at) if expires_in > 0 else None
    
    @override
    async def remove(self, session: Session):
        await self.redis.delete(str(session.id))