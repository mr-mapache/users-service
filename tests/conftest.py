from pytest import fixture
from uuid import UUID
from fastapi import FastAPI
from fastapi.testclient import TestClient

from users.settings import Settings
from users.adapters.setup import Database
from users.adapters.schemas import metadata
from users.adapters.users import Users
from users.adapters.accounts import Accounts
from users.adapters.emails import Emails
from users.schemas import User

@fixture(scope='session')
def settings() -> Settings:
    return Settings()

@fixture(scope='function')
async def database(settings: Settings):
    database = Database(settings)
    await database.setup()
    transaction = await database.connection.begin()
    try:
        await database.connection.run_sync(metadata.create_all)
        yield database
    finally:
        await transaction.rollback()
        await database.connection.run_sync(metadata.drop_all)
        await database.teardown()

@fixture(scope='function')
async def users(database: Database):
    async with database.sessionmaker() as session:
        yield Users(session)
        await session.commit()

@fixture(scope='function')
async def accounts(users: Users):
    user = User(id=UUID('123e4567-e89b-12d3-a456-426614174000'), username='test')
    await users.add(user)
    yield Accounts(users.session, user.pk)
    await users.remove(user)
    
@fixture(scope='function')
async def emails(users: Users):
    user = User(id=UUID('123e4567-e89b-12d3-a456-426614174000'), username='test')
    await users.add(user)
    yield Emails(users.session, user.pk)
    await users.remove(user)