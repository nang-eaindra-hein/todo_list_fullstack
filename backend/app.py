from __future__ import annotations
from litestar.di import Provide
from sqlalchemy.orm import (
    sessionmaker,
    Session,
)
from litestar import Litestar

from sqlalchemy import create_engine
from litestar.middleware.cors import CORSMiddleware
from litestar.middleware import DefineMiddleware
from dotenv import load_dotenv

from .table import Base
from .controller.todo import TodoController
from .controller.note import NoteController
from .controller.draw import DrawController
import os
from litestar.config.cors import CORSConfig


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
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def db_sessions() -> Session:
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


# create tables

# 2.Pydantic schemas

# 3.routes

# 4.app
app = Litestar(
    route_handlers=[TodoController, NoteController, DrawController],
    dependencies={"db": Provide(db_sessions, sync_to_thread=True)},
    middleware=[DefineMiddleware(CORSMiddleware, config=cors_config)],
)
