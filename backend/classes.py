from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class SchemeConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# note
class NoteCreate(SchemeConfig):
    des: str


class NoteUpdate(SchemeConfig):
    des: str


class NoteOutput(SchemeConfig):
    id: int
    des: str
    created_at: datetime
    updated_at: datetime


# draw
class DrawCreate(SchemeConfig):
    img: str


class DrawOutput(SchemeConfig):
    id: int
    img: str


# todo
class TodoCreate(SchemeConfig):
    title: str
    status: bool = False


class TodoUpdate(SchemeConfig):
    id: int
    title: Optional[str] = None
    status: Optional[bool] = None


class TodoOutput(SchemeConfig):
    id: int
    title: str
    status: bool
    created_at: datetime
    updated_at: datetime
    notes: list[NoteOutput] = []
    note_count: int = 0
    draw: list[DrawOutput] = []
