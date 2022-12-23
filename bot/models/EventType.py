from pydantic import BaseModel


class EventType(BaseModel):
    """
    Модель типа, получаемого с помощью API
    """
    type_code: int
    description: str
 