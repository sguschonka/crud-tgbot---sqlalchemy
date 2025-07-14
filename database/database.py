from typing import Annotated

from sqlalchemy import String
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from config import DATABASE_URL

async_engine = create_async_engine(
    url=DATABASE_URL,
    echo=True,
)

async_session = async_sessionmaker(async_engine)

str_100 = Annotated[str, 100]
str_10 = Annotated[str, 10]
str_20 = Annotated[str, 20]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_100: String(100),
        str_10: String(10),
        str_20: String(20),
    }
