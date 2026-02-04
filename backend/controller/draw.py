from sqlalchemy.orm import (
    Session,
)
from sqlalchemy import select
from litestar import Controller, get, post
from litestar.exceptions import NotFoundException
from ..classes import DrawOutput, DrawCreate
from ..table import DrawItems, TodoItems


class DrawController(Controller):
    path = "/todo/{todo_id:int}/draw"

    @get(path="/")
    async def get_draw_list(
        self, todo_id: int, db: Session | None = None
    ) -> list[DrawOutput]:
        q = select(DrawItems).where(DrawItems.todo_id == todo_id)
        rows = db.execute(q).scalars().all()
        return [DrawOutput.model_validate(n) for n in rows]

    @post(path="/")
    async def post_Draw(
        self, db: Session, todo_id: int, data: DrawCreate
    ) -> DrawOutput:
        todo = db.get(TodoItems, todo_id)
        if not todo:
            raise NotFoundException(detail=f"todo id {todo_id} not found")

        Draw = DrawItems(img=data.img, todo_id=todo_id)
        db.add(Draw)
        db.commit()
        db.refresh(Draw)
        return DrawOutput.model_validate(Draw)
