import uuid
from typing import List, Union

from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.dish.models import dish as dish_tbl
from src.dish.schemas import GetSearchDishes, CreateDish, ErrorResponse, DataUpdateDish, UpdateDish, DeleteDish
from src.menu.models import menu as menu_tbl
from src.submenu.models import submenu as submenu_tbl


async def get_all_dishes(submenu_id: uuid.UUID, session: AsyncSession) -> List[GetSearchDishes]:
	"""
	Функция, которая выполняет поиск всех dishes.

	Принимает 2 аргумент:
	- session - экземпляр, который обеспечивает асинхронное взаимодействие с БД.
	- submenu_id - uuid submenu, к которому относятся искомые dishes.

	Возвращает найденный список объектов класса dishes.
	"""
	query = select(dish_tbl).where(dish_tbl.c.submenu_id == submenu_id)
	rez_query = await session.execute(query)
	rezult = [GetSearchDishes(id=data.id, title=data.title,
							  description=data.description,
							  price=data.price)
			  for data in rez_query]
	return rezult


async def create_new_dish(menu_id: uuid.UUID, submenu_id: uuid.UUID,
						  new_values: CreateDish, session: AsyncSession) -> CreateDish:
	"""
	Функция, которая создаёт объект класса dish.
	Обновляет поля submenu и menu.

	Принимает 4 аргументa:
	- session - экземпляр, который обеспечивает асинхронное взаимодействие с БД.
	- new_values - schema pydantic c необходимыми атрибутами для создания объекта класса dish.
	- submenu_id - uuid submenu, к которому должен относятся объект dish.
	- menu_id - uuid menu, к которому должен относятся объект dish.

	Возвращает созданный объект класса dish.
	"""
	id_uuid = uuid.uuid4()
	new_values.price = "{:.2f}".format(float(new_values.price))
	stmt_create = insert(dish_tbl).values(id=id_uuid, title=new_values.title,
										  description=new_values.description,
										  price=new_values.price, submenu_id=submenu_id)

	stmt_update_submenu = update(submenu_tbl).where(submenu_tbl.c.id == submenu_id) \
		.values(dishes_count=submenu_tbl.c.dishes_count + 1)

	stmt_update_menu = update(menu_tbl).where(menu_tbl.c.id == menu_id) \
		.values(dishes_count=menu_tbl.c.dishes_count + 1)

	await session.execute(stmt_create)
	await session.execute(stmt_update_submenu)
	await session.execute(stmt_update_menu)
	await session.commit()
	rezult = GetSearchDishes(id=id_uuid, title=new_values.title,
							 description=new_values.description,
							 price=new_values.price)
	return rezult


async def get_dish_id(dish_id: uuid.UUID, session: AsyncSession) -> GetSearchDishes:
	"""
	Функция, которая выполняет поиск dish по id.

	Принимает 2 аргументa:
	- session - экземпляр, который обеспечивает асинхронное взаимодействие с БД.
	- dish_id - uuid искомого dish.

	Возвращает найденный объект класса dish.
	"""
	query = select(dish_tbl).where(dish_tbl.c.id == dish_id)
	query_exc = await session.execute(query)
	result_query = query_exc.fetchone()
	if result_query is None:
		raise HTTPException(status_code=404, detail="dish not found")
	rezult = GetSearchDishes(id=result_query.id, title=result_query.title,
							 description=result_query.description,
							 price=result_query.price)
	return rezult


async def update_dish(dish_id: uuid.UUID,
					  update_values: DataUpdateDish,
					  session: AsyncSession) -> Union[UpdateDish, ErrorResponse]:
	"""
	Функция, которая обновляет объект класса dish.

	Принимает 3 аргументa:
	- session - экземпляр, который обеспечивает асинхронное взаимодействие с БД.
	- dish_id - uuid объекта, который необходимо обновить.
	- update_values - schema pydantic c атрибутами, которые необходимо обновить.

	Возвращает обновлённый объект класса dish.
	"""
	update_values.price = "{:.2f}".format(float(update_values.price))
	stmt = update(dish_tbl).where(dish_tbl.c.id == dish_id).values(update_values.model_dump(exclude_none=True)) \
		.returning(dish_tbl)
	result_stmt = await session.execute(stmt)
	result = result_stmt.fetchone()
	if result is None:
		return ErrorResponse(detail="submenu not found")
	rezult_data = UpdateDish(id=result.id, title=result.title,
							 description=result.description,
							 price=result.price)
	await session.commit()
	return rezult_data


async def delete_dish(menu_id: uuid.UUID, submenu_id: uuid.UUID,
					  dish_id: uuid.UUID, session: AsyncSession) -> DeleteDish:
	"""
	Функция, которая удаляет объект класса dish.
	Обновляет поля таблицы menu и submenu, связанные c данным dish.

	Принимает 4 аргументa:
	- session - экземпляр, который обеспечивает асинхронное взаимодействие с БД.
	- menu_id - uuid объекта, который необходимо обновить.
	- submenu_id - uuid объекта, который необходимо обновить.
	- dish_id - uuid объекта, который необходимо удалить.

	Возвращает статус выполнения.
	"""
	stmt = delete(dish_tbl).where(dish_tbl.c.id == dish_id)
	result = await session.execute(stmt)
	if result.rowcount:
		stmt_update_submenu = update(submenu_tbl).where(submenu_tbl.c.id == submenu_id) \
			.values(dishes_count=submenu_tbl.c.dishes_count - 1)
		stmt_update_menu = update(menu_tbl).where(menu_tbl.c.id == menu_id) \
			.values(dishes_count=menu_tbl.c.dishes_count - 1)
		await session.execute(stmt_update_submenu)
		await session.execute(stmt_update_menu)
		await session.commit()
		return DeleteDish(status=True, message="The dish has been deleted")
	return DeleteDish(status=False, message="The dish has not been deleted")
