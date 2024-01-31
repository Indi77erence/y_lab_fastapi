import uuid
from http import HTTPStatus

from httpx import AsyncClient

from tests.data_for_tests.data_menu import field_menu, data_for_create_menu, data_for_update_menu, data_for_delete_menu


async def test_get_empty_list_menu(ac: AsyncClient):
	"""Проверка на отсутствие существующих меню."""
	response = await ac.get('/api/v1/menus')
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert response.json() == [], "Список меню не пуст."


async def test_create_menu(ac: AsyncClient):
	"""Проверка на создание меню."""
	response = await ac.post('/api/v1/menus', json=data_for_create_menu)
	answer_response = response.json()
	assert response.status_code == HTTPStatus.CREATED, "Статус ответа не 201."
	for field in data_for_create_menu:
		assert answer_response[field] == data_for_create_menu[field], "Поля меню не соответствуют заданным."
	for field in field_menu:
		assert field in answer_response, f"В меню нет поля {field}."


async def test_get_list_menu_not_empty(ac: AsyncClient):
	"""Проверка на существование одного или нескольких menu"""
	response = await ac.get('/api/v1/menus')
	answer_response = response.json()
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert response.json() != [], "Список меню пуст."
	for menu in answer_response:
		for field in field_menu:
			assert field in menu, f"В меню нет поля {field}."


async def test_get_menu_by_id(ac: AsyncClient, id_menu: uuid.UUID):
	"""Проверка на получение меню по id."""
	response = await ac.get(f"/api/v1/menus/{id_menu}")
	answer_response = response.json()
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."

	for field in data_for_create_menu:
		assert answer_response[field] == data_for_create_menu[field], "Поля меню не соответствуют заданным."

	for field in field_menu:
		assert field in answer_response, f"В меню нет поля {field}."


async def test_update_menu_by_id(ac: AsyncClient, id_menu: uuid.UUID):
	"""Проверка на обновление меню по id."""
	response = await ac.patch(f"/api/v1/menus/{id_menu}", json=data_for_update_menu)
	answer_response = response.json()
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert answer_response["title"] == data_for_update_menu["title"], \
		"Название меню не соответствует ожидаемому"
	assert answer_response["description"] == data_for_update_menu["description"], \
		"Описание меню не соответствует ожидаемому"
	for field in field_menu:
		assert field in answer_response, f"В меню нет поля {field}."


async def test_get_update_menu_by_id(ac: AsyncClient, id_menu: uuid.UUID):
	"""Проверка на получение меню по id."""
	response = await ac.get(f"/api/v1/menus/{id_menu}")
	answer_response = response.json()
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	for field in data_for_create_menu:
		assert answer_response[field] == data_for_update_menu[field], "Поля меню не соответствуют заданным."
	for field in field_menu:
		assert field in answer_response, f"В меню нет поля {field}."


async def test_delete_menu_by_id(ac: AsyncClient, id_menu: uuid.UUID):
	"""Проверка на удаление меню по id."""
	response = await ac.delete(f"/api/v1/menus/{id_menu}")
	answer_response = response.json()
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert answer_response["status"] == data_for_delete_menu["status"], "Статус меню не изменился"
	assert answer_response["message"] == data_for_delete_menu["message"], "Сообщение о удалении неверное"
	"""Проверка на получение меню по id после его удаления."""
	response = await ac.get(f"/api/v1/menus/{id_menu}")
	answer_response = response.json()
	assert response.status_code == HTTPStatus.NOT_FOUND, "Статус ответа не 404."
	assert answer_response["detail"] == "menu not found", "Сообщение об ошибке не соответствует ожидаемому"



async def test_get_empty_list_menu_after_remove(ac: AsyncClient):
	"""Проверка на отсутствие существующих меню."""
	response = await ac.get('/api/v1/menus')
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert response.json() == [], "Список меню не пуст."







