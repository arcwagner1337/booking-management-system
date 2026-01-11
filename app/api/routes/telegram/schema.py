from pydantic import BaseModel


class AddBotModel(BaseModel):
    token: str
