from pydantic import BaseModel, UUID4


class GetSearchMenu(BaseModel):
	id: UUID4
	title: str
	description: str
	submenus_count: int
	dishes_count: int


class DataUpdateMenu(BaseModel):
	title: str | None = None
	description: str | None = None


class CreateMenu(BaseModel):
	title: str
	description: str


class UpdateMenu(BaseModel):
	id: UUID4
	title: str
	description: str
	submenus_count: int
	dishes_count: int


class DeleteMenu(BaseModel):
	status: bool
	message: str


class ErrorResponse(BaseModel):
	detail: str
