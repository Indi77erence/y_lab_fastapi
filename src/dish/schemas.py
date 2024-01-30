from pydantic import BaseModel, UUID4


class GetSearchDishes(BaseModel):
	id: UUID4
	title: str
	description: str
	price: str


class DataUpdateDish(BaseModel):
	title: str | None = None
	description: str | None = None
	price: str | None = None


class CreateDish(BaseModel):
	title: str
	description: str
	price: str


class UpdateDish(BaseModel):
	id: UUID4
	title: str
	description: str
	price: str


class DeleteDish(BaseModel):
	status: bool
	message: str


class ErrorResponse(BaseModel):
	detail: str
