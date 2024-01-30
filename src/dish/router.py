import uuid
from typing import List, Union

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.dish.schemas import GetSearchDishes, CreateDish, ErrorResponse, DataUpdateDish, UpdateDish, DeleteDish
from src.dish.services import get_all_dishes, create_new_dish, get_dish_id, delete_dish, update_dish

# Роутер для управления dish
router = APIRouter(
	prefix='/api/v1',
	tags=['Dish']
)


# Роутер для получения списка всех dish.
@router.get("/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=List[GetSearchDishes])
async def get_dishes(submenu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
	answer = await get_all_dishes(submenu_id, session)
	return answer


# Роутер для создания dish.
@router.post("/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=GetSearchDishes,
			 status_code=status.HTTP_201_CREATED)
async def create_dish(menu_id: uuid.UUID, submenu_id: uuid.UUID,
						 values: CreateDish, session: AsyncSession = Depends(get_async_session)):
	answer = await create_new_dish(menu_id, submenu_id, values, session)
	return answer


# Роутер для получения dish по id.
@router.get("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
			response_model=Union[GetSearchDishes, ErrorResponse])
async def get_dish_by_id(dish_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
	answer = await get_dish_id(dish_id, session)
	return answer


# Роутер для обновления dish по id.
@router.patch("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
			  response_model=Union[UpdateDish, ErrorResponse])
async def update_dish_by_id(dish_id: uuid.UUID, update_values: DataUpdateDish = None,
					  session: AsyncSession = Depends(get_async_session)):
	answer = await update_dish(dish_id, update_values, session)
	return answer


# Роутер для удаления dish по id.
@router.delete("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DeleteDish)
async def delete_dish_by_id(menu_id: uuid.UUID, submenu_id: uuid.UUID, dish_id: uuid.UUID,
							session: AsyncSession = Depends(get_async_session)):
	answer = await delete_dish(menu_id, submenu_id, dish_id, session)
	return answer
