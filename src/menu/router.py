import uuid
from typing import List, Union

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.menu.schemas import GetSearchMenu, UpdateMenu, DeleteMenu, ErrorResponse, CreateMenu, DataUpdateMenu
from src.menu.services import get_all_menus, get_meny_by_id, create_new_menu, \
	update_menu_by_id, delete_menu_by_id, get_data_menu_difficult_query

# Роутер для управления menu
router = APIRouter(
	prefix='/api/v1',
	tags=['Menu']
)


# Роутер получения всех имеющихся меню.
@router.get("/menus_orm/{menu_id}", response_model=Union[GetSearchMenu, ErrorResponse])
async def get_menu_orm(menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
	answer = await get_data_menu_difficult_query(menu_id, session)
	return answer


# Роутер получения всех имеющихся меню.
@router.get("/menus", response_model=List[GetSearchMenu])
async def get_all_menus(answer=Depends(get_all_menus)):
	return answer


# Роутер получения меню по ид.
@router.get("/menus/{menu_id}", response_model=Union[GetSearchMenu, ErrorResponse])
async def get_menu(menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
	answer = await get_meny_by_id(menu_id, session)
	return answer


# Роутер создания меню.
@router.post("/menus", response_model=GetSearchMenu, status_code=status.HTTP_201_CREATED)
async def create_menu(values: CreateMenu, session: AsyncSession = Depends(get_async_session)):
	answer = await create_new_menu(values, session)
	return answer


# Роутер обновления меню по ид.
@router.patch("/menus/{menu_id}", response_model=Union[UpdateMenu, ErrorResponse])
async def update_menu(menu_id: uuid.UUID, update_values: DataUpdateMenu = None,
					  session: AsyncSession = Depends(get_async_session)):
	answer = await update_menu_by_id(menu_id, update_values, session)
	return answer


# Роутер удаления меню по ид.
@router.delete("/menus/{menu_id}", response_model=DeleteMenu)
async def delete_menu(menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
	answer = await delete_menu_by_id(menu_id, session)
	return answer

