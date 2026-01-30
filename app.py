from __future__ import annotations
from typing import Optional
from litestar import Litestar, get, post, put, delete
from litestar.datastructures import State
from litestar.di import Provide
from litestar.exceptions import NotFoundException
from pydantic import BaseModel
from sqlalchemy import Boolean, Integer, String, select, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
    Session,
    relationship,
)
from sqlalchemy import create_engine
from litestar.middleware.cors import CORSMiddleware
from litestar.config.cors import CORSConfig
from litestar.middleware import DefineMiddleware
import os
from litestar import Controller, get, post, put, delete
from dotenv import load_dotenv

load_dotenv()

CLIENT_URL = os.getenv("CLIENT_URL")
DATABASE_URL = os.getenv("DATABASE_URL")

cors_config = CORSConfig(
    allow_origins=[CLIENT_URL],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=False,
)

# 1.sqlalchey
engine = create_engine(
    DATABASE_URL,
    future=True,
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
)
sessionLocal = sessionmaker(future=True, autoflush=False, autocommit=False, bind=engine)


class Base(DeclarativeBase):
    pass


# create tables


class TodoItems(Base):
    __tablename__ = "todo_table"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    notes: Mapped[list["NoteItems"]] = relationship(
        back_populates="todo",
        cascade="all, delete-orphan",
    )


class NoteItems(Base):
    __tablename__ = "note_table"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    des: Mapped[str] = mapped_column(String(500), nullable=False)
    todo: Mapped["TodoItems"] = relationship(back_populates="notes")
    todo_id: Mapped[str] = mapped_column(
        ForeignKey("todo_table.id", ondelete="CASCADE"), nullable=False
    )


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def db_sessions() -> Session:
    db = sessionLocal()
    try:
        yield db
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
    def classMethod_todo(cls, tb: TodoItems) -> "todo_output":
        return cls(id=tb.id, title=tb.title, status=tb.status)


class note_create(BaseModel):
    des: str


class note_update(BaseModel):
    des: str


class note_output(BaseModel):
    id: int
    des: str

    @classmethod
    def classMethod_note(cls, tb: NoteItems) -> "note_output":
        return cls(id=tb.id, des=tb.des)


# 3.routes
class TodoController(Controller):
    path = "/todo"

    @get(path="/")
    async def get_list(
        self, db: Session, status: bool | None = None
    ) -> list[todo_output]:
        get = select(TodoItems)
        if status is not None:
            get = get.where(TodoItems.status == status)

        rows = db.execute(get).scalars().all()
        return [todo_output.classMethod_todo(t) for t in rows]

    @post(path="/")
    async def post_list(self, db: Session, data: todo_create) -> todo_output:
        todo = TodoItems(title=data.title, status=data.status)
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo_output.classMethod_todo(todo)

    @put(path="/{item_id:int}")
    async def update_list(
        self, item_id: int, db: Session, data: todo_update
    ) -> todo_output:
        todo = db.get(TodoItems, item_id)
        if not todo:
            raise NotFoundException(detail=f"todo id {item_id} not found")

        if data.title is not None:
            todo.title = data.title

        if data.status is not None:
            todo.status = data.status
        db.commit()
        db.refresh(todo)
        return todo_output.classMethod_todo(todo)

    @delete(path="/{item_id:int}", status_code=204)
    async def delete_list(self, item_id: int, db: Session) -> None:
        todo = db.get(TodoItems, item_id)

        if not todo:
            raise NotFoundException(detail=f"todo id {item_id} not found")
        db.delete(todo)
        db.commit()
        return None


class NoteController(Controller):
    path = "/todo/{todo_id:int}/note"

    @get(path="/")
    async def get_note_list(
        self, todo_id: int, db: Session | None = None
    ) -> list[note_output]:
        q = select(NoteItems).where(NoteItems.todo_id == todo_id)
        rows = db.execute(q).scalars().all()
        return [note_output.classMethod_note(n) for n in rows]

    @post(path="/")
    async def post_note(
        self, db: Session, todo_id: int, data: note_create
    ) -> note_output:
        todo = db.get(TodoItems, todo_id)
        if not todo:
            raise NotFoundException(detail=f"todo id {todo_id} not found")

        note = NoteItems(des=data.des, todo_id=todo_id)
        db.add(note)
        db.commit()
        db.refresh(note)
        return note_output.classMethod_note(note)

    @put(path="/{item_id:int}")
    async def update_list(
        self, item_id: int, db: Session, data: note_update
    ) -> note_output:
        note = db.get(NoteItems, item_id)
        if not note:
            raise NotFoundException(detail=f"note id {item_id} not found")

        if data.des is not None:
            note.des = data.des
        if note.id is not None:
            note.id = note.id

        db.commit()
        db.refresh(note)
        return note_output.classMethod_note(note)

    @delete(path="/{item_id:int}", status_code=204)
    async def delete_list(self, item_id: int, db: Session) -> None:
        note = db.get(NoteItems, item_id)

        if not note:
            raise NotFoundException(detail=f"note id {item_id} not found")
        db.delete(note)
        db.commit()
        return None


# 4.app
app = Litestar(
    route_handlers=[TodoController, NoteController],
    dependencies={"db": Provide(db_sessions, sync_to_thread=True)},
    middleware=[DefineMiddleware(CORSMiddleware, config=cors_config)],
)
