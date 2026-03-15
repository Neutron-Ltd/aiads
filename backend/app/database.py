from collections.abc import Generator

from sqlmodel import Session, create_engine

from app.config import settings
from app.models import *  # noqa: F401, F403 - Import models so they are registered

_connect_args = (
    {"check_same_thread": False} if "sqlite" in settings.database_url else {}
)
engine = create_engine(
    settings.database_url,
    connect_args=_connect_args,
    echo=settings.debug,
)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
