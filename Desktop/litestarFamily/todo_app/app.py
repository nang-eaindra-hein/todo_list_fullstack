from __future__ import annotations
from typing import Optional
from litestar import Litestar, get, post, put, delete
from litestar.datastructures import State
from litestar.di import Provide
from litestar.exceptions import NotFoundException
from pydantic import BaseModel
from sqlalchemy import Boolean, Integer, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session
from sqlalchemy import create_engine
from litestar.middleware.cors import CORSMiddleware
from litestar.config.cors import CORSConfig
from litestar.middleware import DefineMiddleware
import os

CLIENT_URL = os.getenv("CLIENT_URL")

cors_config = CORSConfig(
    allow_origins=[CLIENT_URL],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=False,
)


# 1.sqlalchemy
DATABASE_URL = "sqlite:///todo.db"

engine = create_engine(DATABASE_URL, future=True, echo=False)
sessionLocal = sessionmaker(future=True, autoflush=False, autocommit=False, bind=engine)


class Base(DeclarativeBase):
    pass


# create tables


class todo_items(Base):
    __tablename__ = "todo_table"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


Base.metadata.create_all(bind=engine)


def db_sessions() -> Session:
    db = sessionLocal()
    try:
        return db
    finally:
        db.close()


# 2.Pydantic schemas
class todo_create(BaseModel):
    title: str
    status: bool = False


class todo_update(BaseModel):
    title: Optional[str] = None
    status: Optional[bool] = None


class todo_output(BaseModel):
    id: int
    title: str
    status: bool

    @classmethod
    def classMethod_todo(cls, tb: todo_items) -> "todo_output":
        return cls(id=tb.id, title=tb.title, status=tb.status)


# 3.routes


@get("/")
async def get_list(db: Session, status: bool | None = None) -> list[todo_output]:
    get = select(todo_items)
    if status is not None:
        get = get.where(todo_items.status == status)

    rows = db.execute(get).scalars().all()
    return [todo_output.classMethod_todo(t) for t in rows]


@post("/")
async def post_list(db: Session, data: todo_create) -> todo_output:
    todo = todo_items(title=data.title, status=data.status)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo_output.classMethod_todo(todo)


@put("/{item_id:int}")
async def update_list(item_id: int, db: Session, data: todo_update) -> todo_output:
    todo = db.get(todo_items, item_id)
    if not todo:
        raise NotFoundException(detail=f"todo id {item_id} not found")

    if data.title is not None:
        todo.title = data.title

    if data.status is not None:
        todo.status = data.status
    db.commit()
    db.refresh(todo)
    return todo_output.classMethod_todo(todo)


@delete("/{item_id:int}", status_code=204)
async def delete_list(item_id: int, db: Session) -> None:
    todo = db.get(todo_items, item_id)

    if not todo:
        raise NotFoundException(detail=f"todo id {item_id} not found")
    db.delete(todo)
    db.commit()
    return None


# 4.app
app = Litestar(
    route_handlers=[get_list, post_list, update_list, delete_list],
    dependencies={"db": Provide(db_sessions, sync_to_thread=True)},
    middleware=[DefineMiddleware(CORSMiddleware, config=cors_config)],
)
