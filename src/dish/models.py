from sqlalchemy import Table, Column, String, ForeignKey
from sqlalchemy import Uuid

from src.database import metadata
from src.submenu.models import submenu

# Таблица блюд.
dish = Table(
	'dish',
	metadata,
	Column('id', Uuid, primary_key=True),
	Column('title', String(50), nullable=False),
	Column('description', String(200), default=None),
	Column('price', String, default=None),
	Column('submenu_id', Uuid, ForeignKey(submenu.c.id, ondelete='CASCADE')),
)
