from datetime import datetime
from typing import Annotated

from sqlalchemy import (
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base, str_10, str_20, str_100

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]


# В декларативном стиле
class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[str]
    tg_id: Mapped[str_100]
    city: Mapped[str_100]
    gender: Mapped[str_10]
    name: Mapped[str_100]
    age: Mapped[int]
    phone_number: Mapped[str_20]
    created_at: Mapped[created_at]
