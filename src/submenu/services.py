import uuid
from typing import List, Union

from fastapi import HTTPException
from sqlalchemy import insert, update, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.menu.models import menu as menu_tbl
from src.submenu.models import submenu as submenu_tbl
from src.submenu.schemas import GetSearchSubmenus, CreateSubmenu, ErrorResponse, DataUpdateSubmenu, UpdateSubmenu, \
	DeleteSubmenu


async def get_all_submenus(menu_id: uuid.UUID, session: AsyncSession) -> List[GetSearchSubmenus]:
	"""
	Функция, которая выполняет поиск всех submenu.

	Принимает 2 аргумент:
	- session - экземпляр, который обеспечивает асинхронное взаимодействие с БД.
	- menu_id - uuid menu, к которому относятся искомые submenu.

	Возвращает список объектов класса submenu.
	"""
	query = select(submenu_tbl).where(submenu_tbl.c.menu_id == menu_id)
	rez_query = await session.execute(query)
	rezult_data = [GetSearchSubmenus(id=data.id, title=data.title,
									 description=data.description,
									 dishes_count=data.dishes_count)
				   for data in rez_query]
	return rezult_data



async def create_new_submenu(menu_id: uuid.UUID, new_values: CreateSubmenu, session: AsyncSession) -> GetSearchSubmenus:
	"""
	Функция, которая создаёт объект класса submenu.

	Принимает 3 аргументa:
	- session - экземпляр, который обеспечивает асинхронное взаимодействие с БД.
	- new_values - schema pydantic c необходимыми атрибутами для создания объекта класса submenu.
	- menu_id - uuid menu, к которому должен относятся объект submenu.

	Возвращает объект класса submenu.
	"""
	id_uuid = uuid.uuid4()

	stmt_create = insert(submenu_tbl).values(id=id_uuid, title=new_values.title,
									  description=new_values.description,
									  dishes_count=0, menu_id=menu_id)
	stmt_update = update(menu_tbl).where(menu_tbl.c.id == menu_id).values(submenus_count=menu_tbl.c.submenus_count + 1)

	await session.execute(stmt_create)
	await session.execute(stmt_update)
	await session.commit()
	rezult = GetSearchSubmenus(id=id_uuid, title=new_values.title,
							 description=new_values.description,
							 submenus_count=0, dishes_count=0)
	return rezult


async def get_submenus_by_id(submenu_id: uuid.UUID, session: AsyncSession) -> GetSearchSubmenus:
	"""
	Функция, которая выполняет поиск submenu по id.

	Принимает 2 аргументa:
	- session - экземпляр, который обеспечивает асинхронное взаимодействие с БД.
	- submenu_id - uuid искомого submenu.

	Возвращает объект класса submenu.
	"""
	query = select(submenu_tbl).where(submenu_tbl.c.id == submenu_id)
	rez_query = await session.execute(query)
	result = rez_query.fetchone()
	if result is None:
		raise HTTPException(status_code=404, detail="submenu not found")
	rezult_data = GetSearchSubmenus(id=result.id, title=result.title,
									 description=result.description,
									 dishes_count=result.dishes_count)
	return rezult_data


async def update_submenu_by_id(submenu_id: uuid.UUID,
							update_values: DataUpdateSubmenu,
							session: AsyncSession) -> Union[UpdateSubmenu, ErrorResponse]:
	"""
	Функция, которая обновляет объект класса submenu.

	Принимает 3 аргументa:
	- session - экземпляр, который обеспечивает асинхронное взаимодействие с БД.
	- submenu_id - uuid объекта, который необходимо обновить.
	- update_values - schema pydantic c атрибутами, которые необходимо обновить.

	Возвращает объект класса submenu.
	"""
	stmt = update(submenu_tbl).where(submenu_tbl.c.id == submenu_id).values(update_values.model_dump(exclude_none=True)) \
		.returning(submenu_tbl)
	result_stmt = await session.execute(stmt)
	result = result_stmt.fetchone()
	if result is None:
		return ErrorResponse(detail="submenu not found")
	rezult_data = UpdateSubmenu(id=result.id, title=result.title,
								description=result.description,
								dishes_count=result.dishes_count)
	await session.commit()
	return rezult_data


async def delete_submenu_by_id(menu_id: uuid.UUID, submenu_id: uuid.UUID, session: AsyncSession) -> DeleteSubmenu:
	"""
	Функция, которая удаляет объект класса submenu.
	Обновляет поля таблицы menu, связанные c submenu и dish.

	Принимает 3 аргументa:
	- session - экземпляр, который обеспечивает асинхронное взаимодействие с БД.
	- menu_id - uuid объекта, который необходимо обновить.
	- submenu_id - uuid объекта, который необходимо удалить.

	Возвращает статус выполнения.
	"""
	query_count_dish = select(submenu_tbl.c.dishes_count).where(submenu_tbl.c.id == submenu_id)
	result = await session.execute(query_count_dish)
	dishes_count = result.fetchone()[0]

	stmt_del_submenu = delete(submenu_tbl).where(submenu_tbl.c.id == submenu_id)
	result = await session.execute(stmt_del_submenu)

	if result.rowcount:
		stmt_update_menu_sub = update(menu_tbl).where(menu_tbl.c.id == menu_id).values(
			submenus_count=menu_tbl.c.submenus_count - 1)

		stmt_update_menu_dish = update(menu_tbl).where(menu_tbl.c.id == menu_id).values(
			dishes_count=menu_tbl.c.dishes_count - dishes_count)

		await session.execute(stmt_update_menu_sub)
		await session.execute(stmt_update_menu_dish)
		await session.commit()

		return DeleteSubmenu(status=True, message="The submenu has been deleted")

	return DeleteSubmenu(status=False, message="The submenu has not been deleted")
