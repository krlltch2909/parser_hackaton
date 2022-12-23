from pydantic import BaseModel
from .EventType import EventType
from .EventTag import EventTag


class Event(BaseModel):
    """
    Модель мероприятия, получаемого с помощью API
    """
    id: int
    title: str
    description: str
    address: str | None
    start_date: str | None
    registration_deadline: str | None
    end_date: str | None
    url: str
    img: str | None
    is_free: bool | None
    type_of_event: EventType
    tags: list[EventTag]
