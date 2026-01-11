from uuid import UUID

from pydantic import BaseModel


class CustomerModel(BaseModel):
    id: UUID
    name: str


class CustomerModelCreate(BaseModel):
    name: str
