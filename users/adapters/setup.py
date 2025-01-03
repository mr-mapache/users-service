from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from users.settings import Settings

class Database:
    def __init__(self, settings: Settings):
        self.engine = create_async_engine(url=settings.database.uri)
        
    async def setup(self):
        self.connection = await self.engine.connect()
        self.sessionmaker = async_sessionmaker(bind=self.connection)

    async def teardown(self):
        await self.connection.close()
        await self.engine.dispose()