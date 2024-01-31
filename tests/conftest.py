import sys

import pytest_asyncio

sys.path.append("..")
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.config import DB_USER_TEST, DB_PASS_TEST, DB_HOST_TEST, DB_PORT_TEST, DB_NAME_TEST
from typing import AsyncGenerator, Any
from httpx import AsyncClient
from sqlalchemy import NullPool, select
from src.database import get_async_session
from src.database import metadata as base_metadata
from src.menu.models import menu as menu_tbl
from src.submenu.models import submenu as submenu_tbl
from src.dish.models import dish as dish_tbl
from src.main import create_app

TEST_DATABASE_URL = f'postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}'

engine_test = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
async_session_maker_test = async_sessionmaker(bind=engine_test, class_=AsyncSession, expire_on_commit=False)
base_metadata.bind = engine_test


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_migration():
	async with engine_test.begin() as connection:
		await connection.run_sync(base_metadata.create_all)
	yield
	async with engine_test.begin() as connection:
		await connection.run_sync(base_metadata.drop_all)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
	async with async_session_maker_test() as async_session:
		yield async_session


@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
	app = create_app()
	app.dependency_overrides[get_async_session] = override_get_async_session
	async with AsyncClient(app=app, base_url='http://localhost:8000') as ac:
		yield ac


@pytest_asyncio.fixture(scope='function')
async def id_menu():
	"""Фикстура для получения id menu."""
	async with async_session_maker_test() as session:
		return await session.scalar(select(menu_tbl))


@pytest_asyncio.fixture(scope='function')
async def id_submenu():
	"""Фикстура для получения id submenu."""
	async with async_session_maker_test() as session:
		return await session.scalar(select(submenu_tbl))


@pytest_asyncio.fixture(scope='function')
async def id_dish():
	"""Фикстура для получения id dish."""
	async with async_session_maker_test() as session:
		return await session.scalar(select(dish_tbl))

