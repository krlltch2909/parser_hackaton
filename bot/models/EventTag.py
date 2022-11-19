from pydantic import BaseModel, Field


class EventTag(BaseModel):
    type_code: int = Field(alias="tag_code")
    description: str
