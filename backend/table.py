from sqlalchemy import Boolean, Integer, String, select, ForeignKey

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.ext.hybrid import hybrid_property


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )


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
    draw: Mapped[list["DrawItems"]] = relationship(
        back_populates="todo",
        cascade="all, delete-orphan",
    )

    @hybrid_property
    def note_count(self) -> int:
        return len(self.notes)


class NoteItems(Base):
    __tablename__ = "note_table"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    des: Mapped[str] = mapped_column(String(500), nullable=False)
    todo: Mapped["TodoItems"] = relationship(back_populates="notes")
    todo_id: Mapped[int] = mapped_column(
        ForeignKey("todo_table.id", ondelete="CASCADE"), nullable=False
    )


class DrawItems(Base):
    __tablename__ = "draw_table"
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    img: Mapped[int] = mapped_column(String[500], nullable=False)
    todo: Mapped["TodoItems"] = relationship(back_populates="draw")
    todo_id: Mapped[int] = mapped_column(
        ForeignKey("todo_table.id", ondelete="CASCADE"), nullable=False
    )
