from sqlalchemy.orm import (
    Session,
)
from sqlalchemy import select
from litestar import Controller, get, post, put, delete
from litestar.exceptions import NotFoundException
from ..classes import NoteOutput, NoteCreate, NoteUpdate
from ..table import NoteItems, TodoItems


class NoteController(Controller):
    path = "/todo/{todo_id:int}/note"

    @get(path="/")
    async def get_note_list(
        self, todo_id: int, db: Session | None = None
    ) -> list[NoteOutput]:
        q = select(NoteItems).where(NoteItems.todo_id == todo_id)
        rows = db.execute(q).scalars().all()
        return [NoteOutput.model_validate(n) for n in rows]

    @post(path="/")
    async def post_note(
        self, db: Session, todo_id: int, data: NoteCreate
    ) -> NoteOutput:
        todo = db.get(TodoItems, todo_id)
        if not todo:
            raise NotFoundException(detail=f"todo id {todo_id} not found")

        note = NoteItems(des=data.des, todo_id=todo_id)
        db.add(note)
        db.commit()
        db.refresh(note)
        return NoteOutput.model_validate(note)

    @put(path="/{item_id:int}")
    async def update_list(
        self, item_id: int, db: Session, data: NoteUpdate
    ) -> NoteOutput:
        note = db.get(NoteItems, item_id)
        if not note:
            raise NotFoundException(detail=f"note id {item_id} not found")

        if data.des is not None:
            note.des = data.des
        if note.id is not None:
            note.id = note.id

        db.commit()
        db.refresh(note)
        return NoteOutput.model_validate(note)

    @delete(path="/{item_id:int}", status_code=204)
    async def delete_list(self, item_id: int, db: Session) -> None:
        note = db.get(NoteItems, item_id)

        if not note:
            raise NotFoundException(detail=f"note id {item_id} not found")
        db.delete(note)
        db.commit()
        return None
