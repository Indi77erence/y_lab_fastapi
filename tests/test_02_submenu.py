import uuid
from http import HTTPStatus

from httpx import AsyncClient

from tests.data_for_tests.data_menu import data_for_create_menu, field_menu, data_for_delete_menu
from tests.data_for_tests.data_submenu import field_submenu, data_for_create_submenu, data_for_update_submenu, \
	data_for_delete_submenu


async def test_create_menu(ac: AsyncClient):
	"""Проверка на создание меню."""
	response = await ac.post('/api/v1/menus', json=data_for_create_menu)
	answer_response = response.json()
	assert response.status_code == HTTPStatus.CREATED, "Статус ответа не 201."
	for field in data_for_create_menu:
		assert answer_response[field] == data_for_create_menu[field], "Поля меню не соответствуют заданным."
	for field in field_menu:
		assert field in answer_response, f"В меню нет поля {field}."


async def test_get_empty_list_submenu(ac: AsyncClient, id_menu: uuid.UUID):
	"""Проверка на отсутствие существующих подменю."""
	response = await ac.get(f"/api/v1/menus/{id_menu}/submenus")
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert response.json() == [], "Список меню не пуст."


async def test_create_submenu(ac: AsyncClient, id_menu: uuid.UUID):
	"""Проверка на создание подменю."""
	response = await ac.post(f"/api/v1/menus/{id_menu}/submenus", json=data_for_create_submenu)
	answer_response = response.json()
	assert response.status_code == HTTPStatus.CREATED, "Статус ответа не 201."
	for field in data_for_create_submenu:
		assert answer_response[field] == data_for_create_submenu[field], "Поля подменю не соответствуют заданным"
	for field in field_submenu:
		assert field in answer_response, f"В подменю нет поля {field}."


async def test_get_list_submenu_not_empty(ac: AsyncClient, id_menu: uuid.UUID):
	"""Проверка на существование одного или нескольких submenu"""
	response = await ac.get(f"/api/v1/menus/{id_menu}/submenus")
	answer_response = response.json()
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert response.json() != [], "Список подменю пуст."
	for submenu in answer_response:
		for field in field_submenu:
			assert field in submenu, f"В меню нет поля {field}."


async def test_get_submenu_by_id(ac: AsyncClient, id_menu: uuid.UUID, id_submenu: uuid.UUID):
	"""Проверка на получение подменю по id."""
	response = await ac.get(f"/api/v1/menus/{id_menu}/submenus/{id_submenu}")
	answer_response = response.json()
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	for field in field_submenu:
		assert field in answer_response, f"В меню нет поля {field}."


async def test_update_submenu_by_id(ac: AsyncClient, id_menu: uuid.UUID, id_submenu: uuid.UUID):
	"""Проверка на обновление подменю по id."""
	response = await ac.patch(f"/api/v1/menus/{id_menu}/submenus/{id_submenu}", json=data_for_update_submenu)
	answer_response = response.json()
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert answer_response["title"] == data_for_update_submenu["title"], \
		"Название подменю не соответствует ожидаемому"
	assert answer_response["description"] == data_for_update_submenu["description"], \
		"Описание подменю не соответствует ожидаемому"
	for field in field_submenu:
		assert field in answer_response, f"В подменю нет поля {field}."


async def test_get_submenu_by_id_after_update(ac: AsyncClient, id_menu: uuid.UUID, id_submenu: uuid.UUID):
	"""Проверка на получение подменю по id после обновления."""
	response = await ac.get(f"/api/v1/menus/{id_menu}/submenus/{id_submenu}")
	answer_response = response.json()
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert answer_response["title"] == data_for_update_submenu["title"], \
		"Название подменю не соответствует ожидаемому"
	assert answer_response["description"] == data_for_update_submenu["description"], \
		"Описание подменю не соответствует ожидаемому"
	for field in field_submenu:
		assert field in answer_response, f"В меню нет поля {field}."


async def test_delete_submenu_by_id(ac: AsyncClient, id_menu: uuid.UUID, id_submenu: uuid.UUID, saved_data: dict):
	"""Проверка на удаление подменю по id."""
	response = await ac.delete(f"/api/v1/menus/{id_menu}/submenus/{id_submenu}")
	answer_response = response.json()
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert answer_response["status"] == data_for_delete_submenu["status"], "Статус подменю не изменился"
	assert answer_response["message"] == data_for_delete_submenu["message"], "Подменю не удалилось"
	saved_data["submenu_id"] = id_submenu


async def test_get_list_submenu_after_delete(ac: AsyncClient, id_menu: uuid.UUID):
	"""Проверка на отсутствие существующих подменю после удаления."""
	response = await ac.get(f"/api/v1/menus/{id_menu}/submenus")
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert response.json() == [], "Список подменю не пуст."


async def test_get_submenu_by_id_after_remove(ac: AsyncClient, id_menu: uuid.UUID, saved_data: dict):
	"""Проверка на получение подменю по id после его удаления."""
	id_submenu = saved_data["submenu_id"]
	response = await ac.get(f"/api/v1/menus/{id_menu}/submenus/{id_submenu}")
	answer_response = response.json()
	assert response.status_code == HTTPStatus.NOT_FOUND, "Статус ответа не 404."
	assert answer_response["detail"] == "submenu not found", "Сообщение об ошибке не соответствует ожидаемому"


async def test_delete_menu_by_id(ac: AsyncClient, id_menu: uuid.UUID):
	"""Проверка на удаление меню по id."""
	response = await ac.delete(f"/api/v1/menus/{id_menu}")
	answer_response = response.json()
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert answer_response["status"] == data_for_delete_menu["status"], "Статус меню не изменился"
	assert answer_response["message"] == data_for_delete_menu["message"], "Сообщение о удалении не соответствует ожидаемому"


async def test_get_empty_list_menu(ac: AsyncClient):
	"""Проверка на отсутствие существующих меню после удаления."""
	response = await ac.get('/api/v1/menus')
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert response.json() == [], "Список меню не пуст."
