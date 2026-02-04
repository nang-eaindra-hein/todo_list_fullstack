from sqlalchemy.orm import (
    Session,
)
from sqlalchemy import select, update
from litestar import Controller, get, post, put, delete
from litestar.exceptions import NotFoundException
from ..classes import TodoOutput, TodoCreate, TodoUpdate
from ..table import TodoItems

from sqlalchemy.orm import selectinload


class TodoController(Controller):
    path = "/todo"

    @get(path="/")
    async def get_list(
        self, db: Session, status: bool | None = None
    ) -> list[TodoOutput]:
        get = select(TodoItems).options(selectinload(TodoItems.notes))
        if status is not None:
            get = get.where(TodoItems.status == status)

        rows = db.execute(get).scalars().all()
        return [TodoOutput.model_validate(t) for t in rows]

    @post(path="/")
    async def post_list(self, db: Session, data: TodoCreate) -> TodoOutput:
        todo = TodoItems(
            title=data.title,
            status=data.status or False,
        )
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return TodoOutput.model_validate(todo)

    @put(path="/{item_id:int}")
    async def update_list(
        self, item_id: int, db: Session, data: TodoUpdate
    ) -> TodoOutput:
        todo = db.get(TodoItems, item_id)
        if not todo:
            raise NotFoundException(detail=f"todo id {item_id} not found")

        if data.title is not None:
            todo.title = data.title

        if data.status is not None:
            todo.status = data.status
        db.commit()
        db.refresh(todo)
        return TodoOutput.model_validate(todo)

    @delete(path="/{item_id:int}", status_code=204)
    async def delete_list(self, item_id: int, db: Session) -> None:
        todo = db.get(TodoItems, item_id)

        if not todo:
            raise NotFoundException(detail=f"todo id {item_id} not found")
        db.delete(todo)
        db.commit()
        return None
