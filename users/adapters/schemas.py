from sqlalchemy import Table, MetaData, Column
from sqlalchemy import Integer, UUID, String, Text, Boolean
from sqlalchemy import ForeignKey

metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('pk', Integer, primary_key=True),
    Column('user_id', UUID, unique=True, nullable=False),
    Column('user_username', String, unique=True)
)

emails = Table(
    'emails',
    metadata,
    Column('pk', Integer, primary_key=True),
    Column('email_address', String, unique=True, nullable=False),
    Column('email_is_primary', Boolean, nullable=False),
    Column('email_is_verified', Boolean, nullable=False),
    Column('user_pk', Integer, ForeignKey('users.pk', ondelete='CASCADE'), nullable=False)
)

accounts = Table(
    'accounts',
    metadata,
    Column('pk', Integer, primary_key=True),
    Column('account_id', String, nullable=False),
    Column('account_type', String, nullable=False),
    Column('account_provider', String, nullable=False),
    Column('user_pk', Integer, ForeignKey('users.pk', ondelete='CASCADE'), nullable=False)
)