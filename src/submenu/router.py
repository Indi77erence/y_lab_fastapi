import uuid
from typing import List, Union

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.submenu.schemas import GetSearchSubmenus, CreateSubmenu, ErrorResponse, UpdateSubmenu, DataUpdateSubmenu, \
	DeleteSubmenu
from src.submenu.services import create_new_submenu, get_all_submenus, update_submenu_by_id, \
	delete_submenu_by_id, get_submenus_by_id

# Роутер для управления submenu
router = APIRouter(
	prefix='/api/v1',
	tags=['Submenu']
)


# Роутер для получения списка всех submenu.
@router.get("/menus/{menu_id}/submenus", response_model=List[GetSearchSubmenus])
async def get_submenus(menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
	answer = await get_all_submenus(menu_id, session)
	return answer


# Роутер для создания submenu.
@router.post("/menus/{menu_id}/submenus", response_model=GetSearchSubmenus, status_code=status.HTTP_201_CREATED)
async def create_submenu(menu_id: uuid.UUID, values: CreateSubmenu, session: AsyncSession = Depends(get_async_session)):
	answer = await create_new_submenu(menu_id, values, session)
	return answer


# Роутер для получения submenu по id.
@router.get("/menus/{menu_id}/submenus/{submenu_id}", response_model=Union[GetSearchSubmenus, ErrorResponse])
async def get_submenu(submenu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
	answer = await get_submenus_by_id(submenu_id, session)
	return answer


# Роутер для обновления submenu по id.
@router.patch("/menus/{menu_id}/submenus/{submenu_id}", response_model=Union[UpdateSubmenu, ErrorResponse])
async def update_menu(submenu_id: uuid.UUID, update_values: DataUpdateSubmenu = None,
					  session: AsyncSession = Depends(get_async_session)):
	answer = await update_submenu_by_id(submenu_id, update_values, session)
	return answer


# Роутер для удаления submenu по id.
@router.delete("/menus/{menu_id}/submenus/{submenu_id}", response_model=DeleteSubmenu)
async def delete_submenu(menu_id: uuid.UUID, submenu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
	answer = await delete_submenu_by_id(menu_id, submenu_id, session)
	return answer
