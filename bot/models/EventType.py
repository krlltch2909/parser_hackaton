from pydantic import BaseModel


class EventType(BaseModel):
    description: str
    type_code: int
