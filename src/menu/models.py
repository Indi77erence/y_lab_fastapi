from sqlalchemy import Table, Column, String
from sqlalchemy import Uuid, Integer

from src.database import metadata

# Таблица меню.
menu = Table(
	'menu',
	metadata,
	Column('id', Uuid, primary_key=True),
	Column('title', String(50), nullable=False),
	Column('description', String(200), default=None),
	Column('submenus_count', Integer, default=0),
	Column('dishes_count', Integer, default=0)
)
