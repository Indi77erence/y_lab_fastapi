from fastapi import FastAPI

from src.dish.router import router as dish_router
from src.menu.router import router as menu_router
from src.submenu.router import router as submenu_router


def create_app():
	app = FastAPI(title="RestMenu APP")

	app.include_router(menu_router)
	app.include_router(submenu_router)
	app.include_router(dish_router)

	return app
