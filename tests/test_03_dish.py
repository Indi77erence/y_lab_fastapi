import uuid
from http import HTTPStatus

from httpx import AsyncClient

from tests.data_for_tests.data_dish import data_for_create_dish, field_dish, data_for_update_dish, \
	data_for_delete_dish
from tests.data_for_tests.data_menu import data_for_create_menu, field_menu, data_for_delete_menu
from tests.data_for_tests.data_submenu import data_for_create_submenu, field_submenu, data_for_delete_submenu


async def test_create_menu(ac: AsyncClient):
	"""Проверка на создание меню."""
	response = await ac.post('/api/v1/menus', json=data_for_create_menu)
	answer_response = response.json()
	assert response.status_code == HTTPStatus.CREATED, "Статус ответа не 201."
	for field in data_for_create_menu:
		assert answer_response[field] == data_for_create_menu[field], "Поля меню не соответствуют заданным."
	for field in field_menu:
		assert field in answer_response, f"В меню нет поля {field}."


async def test_create_submenu(ac: AsyncClient, id_menu: uuid.UUID):
	"""Проверка на создание подменю."""
	response = await ac.post(f"/api/v1/menus/{id_menu}/submenus", json=data_for_create_submenu)
	answer_response = response.json()
	assert response.status_code == HTTPStatus.CREATED, "Статус ответа не 201."
	for field in data_for_create_submenu:
		assert answer_response[field] == data_for_create_submenu[field], "Поля подменю не соответствуют заданным"
	for field in field_submenu:
		assert field in answer_response, f"В подменю нет поля {field}."


async def test_get_empty_list_dishes(ac: AsyncClient, id_menu: uuid.UUID, id_submenu: uuid.UUID):
	"""Проверка на отсутствие существующих меню."""
	response = await ac.get(f"/api/v1/menus/{id_menu}/submenus/{id_submenu}/dishes")
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert response.json() == [], "Список блюд не пуст."


async def test_create_dish(ac: AsyncClient, id_menu: uuid.UUID, id_submenu: uuid.UUID):
	"""Проверка на создание dish."""
	response = await ac.post(f"/api/v1/menus/{id_menu}/submenus/{id_submenu}/dishes", json=data_for_create_dish)
	answer_response = response.json()
	assert response.status_code == HTTPStatus.CREATED, "Статус ответа не 201."
	for field in data_for_create_dish:
		assert answer_response[field] == data_for_create_dish[field], "Поля блюда не соответствуют заданным."
	for field in field_dish:
		assert field in answer_response, f"В подменю нет поля {field}."


async def test_get_not_empty_list_dishes(ac: AsyncClient, id_menu: uuid.UUID, id_submenu: uuid.UUID):
	"""Проверка на наличие существующих блюд."""
	response = await ac.get(f"/api/v1/menus/{id_menu}/submenus/{id_submenu}/dishes")
	answer_response = response.json()
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert response.json() != [], "Список блюд пуст."
	for dish in answer_response:
		for field in field_dish:
			assert field in dish, f"В блюде нет поля {field}."


async def test_get_dish_by_id(ac: AsyncClient, id_menu: uuid.UUID, id_submenu: uuid.UUID, id_dish: uuid.UUID):
	"""Проверка на получение блюда по id."""
	response = await ac.get(f"/api/v1/menus/{id_menu}/submenus/{id_submenu}/dishes/{id_dish}")
	answer_response = response.json()
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	for field in field_dish:
		assert field in answer_response, f"В блюде нет поля {field}."


async def test_update_dish_by_id(ac: AsyncClient, id_menu: uuid.UUID, id_submenu: uuid.UUID, id_dish: uuid.UUID):
	"""Проверка на обновление блюда по id."""
	response = await ac.patch(f"/api/v1/menus/{id_menu}/submenus/{id_submenu}/dishes/{id_dish}",
							  json=data_for_update_dish)
	answer_response = response.json()
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert answer_response["title"] == data_for_update_dish["title"], \
		"Название подменю не соответствует ожидаемому"
	assert answer_response["description"] == data_for_update_dish["description"], \
		"Описание подменю не соответствует ожидаемому"
	assert answer_response["price"] == data_for_update_dish["price"], "Цена блюда не соответствует ожидаемой"
	for field in field_dish:
		assert field in answer_response, f"В подменю нет поля {field}."


async def test_get_dish_by_id_after_update(ac: AsyncClient, id_menu: uuid.UUID, id_submenu: uuid.UUID,
										   id_dish: uuid.UUID):
	"""Проверка на получение блюда по id после обновления."""
	response = await ac.get(f"/api/v1/menus/{id_menu}/submenus/{id_submenu}/dishes/{id_dish}")
	answer_response = response.json()
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert answer_response["title"] == data_for_update_dish["title"], \
		"Название блюда не соответствует ожидаемому"
	assert answer_response["description"] == data_for_update_dish["description"], \
		"Описание блюда не соответствует ожидаемому"
	assert answer_response["price"] == data_for_update_dish["price"], "Цена блюда не соответствует ожидаемой"
	for field in field_dish:
		assert field in answer_response, f"В блюде нет поля {field}."


async def test_delete_dish_by_id(ac: AsyncClient, id_menu: uuid.UUID, id_submenu: uuid.UUID, id_dish: uuid.UUID):
	"""Проверка на удаление блюда по id."""
	response = await ac.delete(f"/api/v1/menus/{id_menu}/submenus/{id_submenu}/dishes/{id_dish}")
	answer_response = response.json()
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert answer_response["status"] == data_for_delete_dish["status"], "Статус удаления не соответствует заданному"
	assert answer_response["message"] == data_for_delete_dish["message"], "Блюдо не удалилось"

	"""Проверка на получение блюда по id после удаления."""
	response = await ac.get(f"/api/v1/menus/{id_menu}/submenus/{id_submenu}/dishes/{id_dish}")
	answer_response = response.json()
	assert response.status_code == HTTPStatus.NOT_FOUND, "Статус ответа не 404."
	assert answer_response["detail"] == "dish not found", "Сообщение об ошибке не соответствует ожидаемому"


async def test_get_empty_list_dishes_after_delete(ac: AsyncClient, id_menu: uuid.UUID, id_submenu: uuid.UUID):
	"""Проверка на отсутствие существующих блюд."""
	response = await ac.get(f"/api/v1/menus/{id_menu}/submenus/{id_submenu}/dishes")
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert response.json() == [], "Список блюд не пуст."


async def test_delete_submenu_by_id(ac: AsyncClient, id_menu: uuid.UUID, id_submenu: uuid.UUID):
	"""Проверка на удаление подменю по id."""
	response = await ac.delete(f"/api/v1/menus/{id_menu}/submenus/{id_submenu}")
	answer_response = response.json()
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert answer_response["status"] == data_for_delete_submenu["status"], "Статус подменю не изменился"
	assert answer_response["message"] == data_for_delete_submenu["message"], "Подменю не удалилось"


async def test_get_list_submenu_after_delete(ac: AsyncClient, id_menu: uuid.UUID):
	"""Проверка на отсутствие существующих подменю после удаления."""
	response = await ac.get(f"/api/v1/menus/{id_menu}/submenus")
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert response.json() == [], "Список подменю не пуст."


async def test_delete_menu_by_id(ac: AsyncClient, id_menu: uuid.UUID):
	"""Проверка на удаление меню по id."""
	response = await ac.delete(f"/api/v1/menus/{id_menu}")
	answer_response = response.json()
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert answer_response["status"] == data_for_delete_menu["status"], "Статус меню не изменился"
	assert answer_response["message"] == data_for_delete_menu[
		"message"], "Сообщение о удалении не соответствует ожидаемому"


async def test_get_empty_list_menu_after_remove(ac: AsyncClient):
	"""Проверка на отсутствие существующих меню."""
	response = await ac.get('/api/v1/menus')
	assert response.status_code == HTTPStatus.OK, "Статус ответа не 200."
	assert response.json() == [], "Список меню не пуст."

