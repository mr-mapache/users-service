from uuid import uuid4
from pytest import mark
from users.ports import Users, Accounts, Emails
from users.schemas import User, Account, Email

@mark.asyncio
async def test_users(users: Users):
    id = uuid4()
    user = User(id=id, username='test')
    await users.add(user)
    assert user.pk is not None
    user = await users.get(id)
    assert user.username == 'test'
    user.username = 'changed'
    await users.update(user)
    user = await users.get(id)
    assert user.username == 'changed'
    await users.remove(user)
    assert await users.get(id) == None

@mark.asyncio
async def test_accounts(accounts: Accounts):
    account = Account(id='1', type='oauth', provider='google')
    await accounts.add(account)
    assert await accounts.get(provider='google', id='1') == account
    await accounts.remove(account)
    assert await accounts.get(provider='google', id='1') == None

@mark.asyncio
async def test_emails(emails: Emails):
    email = Email(address='test@test.com', is_primary=True, is_verified=False)
    await emails.add(email)
    assert await emails.get(email.address) == email
    assert await emails.list() == [email]
    email = Email(address='test2@test.com', is_primary=False, is_verified=False)
    await emails.add(email)
    email_list = await emails.list()
    assert len(email_list) == 2
    email.is_primary = True
    await emails.update(email)
    old_email = await emails.get('test@test.com')
    assert old_email.is_primary == False
    new_email = await emails.get('test2@test.com')
    assert new_email.is_primary == True
    email = Email(address='test3@test.com', is_primary=True, is_verified=False)
    await emails.add(email)    
    old_email = await emails.get('test2@test.com')
    assert old_email.is_primary == False