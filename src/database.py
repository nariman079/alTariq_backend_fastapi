from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@localhost:5433/postgres'

engine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=True
)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """ Dependency for getting async session """
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
