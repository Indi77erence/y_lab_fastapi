from sqlalchemy import Table, Column, String, ForeignKey, Integer
from sqlalchemy import Uuid

from src.database import metadata
from src.menu.models import menu

# Таблица подменю.
submenu = Table(
	'submenu',
	metadata,
	Column('id', Uuid, primary_key=True,),
	Column('title', String(50), nullable=False),
	Column('description', String(200), default=None),
	Column('dishes_count', Integer, default=0),
	Column('menu_id', Uuid, ForeignKey(menu.c.id, ondelete='CASCADE'), default=None),
)
