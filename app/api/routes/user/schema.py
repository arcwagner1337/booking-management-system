from uuid import UUID

from pydantic import BaseModel


class UserModel(BaseModel):
    id: UUID

    tlg_id: int | None

    first_name: str | None
    last_name: str | None
    username: str | None

    language_code: str | None
