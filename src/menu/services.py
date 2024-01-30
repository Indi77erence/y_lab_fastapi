import uuid
from typing import List, Union

from fastapi import Depends, HTTPException
from sqlalchemy import select, insert, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.menu.models import menu as menu_tbl
from src.menu.schemas import GetSearchMenu, UpdateMenu, DeleteMenu, ErrorResponse, DataUpdateMenu, CreateMenu
from src.submenu.models import submenu as submenu_tbl


async def get_data_menu_difficult_query(menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)) \
		-> GetSearchMenu:
	"""
	Функция, которая выполняет поиск кол-ва подменю и блюд для конкретного меню.

	Принимает 2 аргумента:
	- session - экземпляр, который обеспечивает асинхронное взаимодействие с БД.
	- menu_id - id меню
	Возвращает объект класса menu.
	"""
	stmt = select(
		menu_tbl.c.id,
		menu_tbl.c.title,
		menu_tbl.c.description,
		func.count(submenu_tbl.c.id == menu_id).label('submenus_count'),
		func.sum(submenu_tbl.c.dishes_count).label('dishes_count')
	).select_from(
		menu_tbl.join(submenu_tbl, menu_tbl.c.id == submenu_tbl.c.menu_id, isouter=True)
	).group_by(
		menu_tbl.c.id, menu_tbl.c.title
	)
	rez_query = await session.execute(stmt)
	result = rez_query.fetchone()

	if result is None:
		raise HTTPException(status_code=404, detail="menu not found")

	result_dict = result._asdict()
	if result_dict["dishes_count"] is None:
		result_dict["dishes_count"] = 0

	result_data = GetSearchMenu(id=result_dict["id"], title=result_dict["title"], description=result_dict["description"],
								submenus_count=result_dict["submenus_count"], dishes_count=result_dict["dishes_count"])
	return result_data


async def get_all_menus(session: AsyncSession = Depends(get_async_session)) -> List[GetSearchMenu]:
	"""
	Функция, которая выполняет поиск всех меню.

	Принимает 1 аргумент:
	- session - экземпляр, который обеспечивает асинхронное взаимодействие с БД.

	Возвращает список объектов класса menu.
	"""
	query = select(menu_tbl)
	rez_query = await session.execute(query)
	rezult_data = [GetSearchMenu(id=data.id, title=data.title, description=data.description,
								 submenus_count=data.submenus_count, dishes_count=data.dishes_count)
				   for data in rez_query]

	return rezult_data


async def get_meny_by_id(menu_id: uuid.UUID, session: AsyncSession) -> Union[GetSearchMenu, ErrorResponse]:
	"""
	Функция, которая выполняет поиск меню по id.

	Принимает 2 аргументa:
	- session - экземпляр, который обеспечивает асинхронное взаимодействие с БД.
	- menu_id - uuid искомого menu.

	Возвращает объект класса menu.
	"""
	stmt = select(menu_tbl).where(menu_tbl.c.id == menu_id)
	rez_query = await session.execute(stmt)
	result = rez_query.fetchone()
	if result is None:
		raise HTTPException(status_code=404, detail="menu not found")
	rezult_data = GetSearchMenu(id=result.id, title=result.title, description=result.description,
								submenus_count=result.submenus_count, dishes_count=result.dishes_count)
	return rezult_data


async def create_new_menu(new_values: CreateMenu, session: AsyncSession) -> GetSearchMenu:
	"""
	Функция, которая создаёт объект класса menu.

	Принимает 2 аргументa:
	- session - экземпляр, который обеспечивает асинхронное взаимодействие с БД.
	- new_values - schema pydantic c необходимыми атрибутами для создания объекта класса menu.

	Возвращает объект класса menu.
	"""
	id_uuid = uuid.uuid4()
	stmt = insert(menu_tbl).values(id=id_uuid, title=new_values.title, description=new_values.description)
	await session.execute(stmt)
	await session.commit()
	info = GetSearchMenu(id=id_uuid, title=new_values.title,
						 description=new_values.description,
						 submenus_count=0, dishes_count=0)
	return info


async def update_menu_by_id(menu_id: uuid.UUID,
							update_values: DataUpdateMenu,
							session: AsyncSession) -> Union[UpdateMenu, ErrorResponse]:
	"""
	Функция, которая обновляет объект класса menu.

	Принимает 3 аргументa:
	- session - экземпляр, который обеспечивает асинхронное взаимодействие с БД.
	- menu_id - uuid объекта, который необходимо обновить.
	- update_values - schema pydantic c атрибутами, которые необходимо обновить.

	Возвращает объект класса menu.
	"""
	stmt = update(menu_tbl).where(menu_tbl.c.id == menu_id).values(update_values.model_dump(exclude_none=True)) \
		.returning(menu_tbl)
	result_stmt = await session.execute(stmt)
	result = result_stmt.fetchone()
	if result is None:
		return ErrorResponse(detail="menu not found")
	rezult_data = UpdateMenu(id=result.id, title=result.title, description=result.description,
							 submenus_count=result.submenus_count, dishes_count=result.dishes_count)
	await session.commit()
	return rezult_data


async def delete_menu_by_id(menu_id: uuid.UUID, session: AsyncSession) -> DeleteMenu:
	"""
	Функция, которая удаляет объект класса menu.

	Принимает 2 аргументa:
	- session - экземпляр, который обеспечивает асинхронное взаимодействие с БД.
	- menu_id - uuid объекта, который необходимо удалить.

	Возвращает статус выполнения.
	"""
	stmt = delete(menu_tbl).where(menu_tbl.c.id == menu_id)
	result = await session.execute(stmt)
	if result.rowcount:
		await session.commit()
		return DeleteMenu(status=True, message="The menu has been deleted")
	return DeleteMenu(status=False, message="The menu has not been deleted")
