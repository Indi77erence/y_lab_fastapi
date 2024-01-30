from pydantic import BaseModel, UUID4


class GetSearchSubmenus(BaseModel):
	id: UUID4
	title: str
	description: str
	dishes_count: int


class DataUpdateSubmenu(BaseModel):
	title: str | None = None
	description: str | None = None


class CreateSubmenu(BaseModel):
	title: str
	description: str


class UpdateSubmenu(BaseModel):
	id: UUID4
	title: str
	description: str
	dishes_count: int


class DeleteSubmenu(BaseModel):
	status: bool
	message: str


class ErrorResponse(BaseModel):
	detail: str
