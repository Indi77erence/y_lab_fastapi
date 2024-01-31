import uuid
from http import HTTPStatus

from httpx import AsyncClient

from data_for_tests.data_dish import data_for_create_dish, field_dish, data_for_create_second_dish
from data_for_tests.data_menu import data_for_create_menu, field_menu, data_for_delete_menu
from data_for_tests.data_submenu import data_for_create_submenu, field_submenu, data_for_delete_submenu


async def test_scenario_create_menu(ac: AsyncClient):
	"""Проверка на создание меню для сценария."""
	response = await ac.post('/api/v1/menus', json=data_for_create_menu)
	answer_response = response.json()
	assert response.status_code == HTTPStatus.CREATED, "Статус ответа не 201."
	for field in data_for_create_menu:
		assert answer_response[field] == data_for_create_menu[field], "Поля меню не соответствуют заданным."
	for field in field_menu:
		assert field in answer_response, f"В меню нет поля {field}."


async def test_scenario_create_submenu(ac: AsyncClient, id_menu: uuid.UUID):
	"""Проверка на создание подменю для сценария."""
	response = await ac.post(f"/api/v1/menus/{id_menu}/submenus", json=data_for_create_submenu)
	answer_response = response.json()
	assert response.status_code == HTTPStatus.CREATED, "Статус ответа не 201."
	for field in data_for_create_submenu:
		assert answer_response[field] == data_for_create_submenu[field], "Поля подменю не соответствуют заданным"
	for field in field_submenu:
		assert field in answer_response, f"В подменю нет поля {field}."


async def test_scenario_create_dish(ac: AsyncClient, id_menu: uuid.UUID, id_submenu: uuid.UUID):
	"""Проверка на создание dish для сценария."""
	response = await ac.post(f"/api/v1/menus/{id_menu}/submenus/{id_submenu}/dishes", json=data_for_create_dish)
	answer_response = response.json()
	assert response.status_code == HTTPStatus.CREATED, "Статус ответа не 201."
	for field in data_for_create_dish:
		assert answer_response[field] == data_for_create_dish[field], "Поля блюда не соответствуют заданным."
	for field in field_dish:
		assert field in answer_response, f"В подменю нет поля {field}."


async def test_scenario_create_second_dish(ac: AsyncClient, id_menu: uuid.UUID, id_submenu: uuid.UUID):
	"""Проверка на создание второго dish для сценария."""
	response = await ac.post(f"/api/v1/menus/{id_menu}/submenus/{id_submenu}/dishes", json=data_for_create_second_dish)
	answer_response = response.json()
	assert response.status_code == HTTPStatus.CREATED, "Статус ответа не 201."
	for field in data_for_create_second_dish:
		assert answer_response[field] == data_for_create_second_dish[field], "Поля блюда не соответствуют заданным."
	for field in field_dish:
		assert field in answer_response, f"В подменю нет поля {field}."


async def test_scenario_get_menu_by_id(ac: AsyncClient, id_menu: uuid.UUID):
	"""Проверка на получение меню по id для сценария."""
	response = await ac.get(f"/api/v1/menus/{id_menu}")
	answer_response = response.json()
	assert answer_response["submenus_count"] == 1, "Поле 'submenus_count' не соответствует ожидаемому"
	assert answer_response["dishes_count"] == 2, "Поле 'dishes_count' не соответствует ожидаемому"
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	for field in data_for_create_menu:
		assert answer_response[field] == data_for_create_menu[field], "Поля меню не соответствуют заданным."
	for field in field_menu:
		assert field in answer_response, f"В меню нет поля {field}."


async def test_scenario_get_submenu_by_id(ac: AsyncClient, id_menu: uuid.UUID, id_submenu: uuid.UUID):
	"""Проверка на получение подменю по id для сценария."""
	response = await ac.get(f"/api/v1/menus/{id_menu}/submenus/{id_submenu}")
	answer_response = response.json()
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert answer_response["dishes_count"] == 2, "Поле 'dishes_count' не соответствует ожидаемому"
	for field in field_submenu:
		assert field in answer_response, f"В меню нет поля {field}."


async def test_scenario_delete_submenu_by_id(ac: AsyncClient, id_menu: uuid.UUID, id_submenu: uuid.UUID):
	"""Проверка на удаление подменю по id для сценария."""
	response = await ac.delete(f"/api/v1/menus/{id_menu}/submenus/{id_submenu}")
	answer_response = response.json()
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert answer_response["status"] == data_for_delete_submenu["status"], "Статус подменю не изменился"
	assert answer_response["message"] == data_for_delete_submenu["message"], "Подменю не удалилось"


async def test_scenario_get_empty_list_submenu(ac: AsyncClient, id_menu: uuid.UUID):
	"""Проверка на отсутствие существующих подменю для сценария."""
	response = await ac.get(f"/api/v1/menus/{id_menu}/submenus")
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert response.json() == [], "Список подменю не пуст."


async def test_scenario_get_empty_list_dishes(ac: AsyncClient, id_menu: uuid.UUID, id_submenu: uuid.UUID):
	"""Проверка на отсутствие существующих блюд для сценария."""
	response = await ac.get(f"/api/v1/menus/{id_menu}/submenus/{id_submenu}/dishes")
	assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, "Статус ответа не 422."


async def test_scenario_get_menu_by_id_after_del_submenu(ac: AsyncClient, id_menu: uuid.UUID):
	"""Проверка на получение меню по id для сценария после удаления подменю."""
	response = await ac.get(f"/api/v1/menus/{id_menu}")
	answer_response = response.json()
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	for field in data_for_create_menu:
		assert answer_response[field] == data_for_create_menu[field], "Поля меню не соответствуют заданным."
	assert answer_response["submenus_count"] == 0, "Поле 'submenus_count' не соответствует ожидаемому"
	for field in field_menu:
		assert field in answer_response, f"В меню нет поля {field}."


async def test_scenario_delete_menu_by_id(ac: AsyncClient, id_menu: uuid.UUID):
	"""Проверка на удаление меню по id для сценария."""
	response = await ac.delete(f"/api/v1/menus/{id_menu}")
	answer_response = response.json()
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert answer_response["status"] == data_for_delete_menu["status"], "Статус меню не изменился"
	assert answer_response["message"] == data_for_delete_menu["message"], \
		"Сообщение о удалении не соответствует ожидаемому"


async def test_scenario_get_empty_list_menu(ac: AsyncClient):
	"""Проверка на отсутствие существующих меню для сценария."""
	response = await ac.get('/api/v1/menus')
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert response.json() == [], "Список меню не пуст."
