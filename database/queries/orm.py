from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError

from database.database import async_session
from database.models import UsersOrm


class Orm:
    @staticmethod
    async def insert_user(user_data: dict[str, Any]) -> UsersOrm | None:
        async with async_session() as s:
            user = UsersOrm(**user_data)
            s.add(user)
            await s.commit()
            await s.refresh(user)
            return user

    @staticmethod
    async def get_user_by_tg_id(tg_id: int):
        """Получает пользователя по tg_id

        Args:
            tg_id (int): уникальный код присуждаемый telegram api каждому пользователю, который не меняется даже при смене username'а
        """
        async with async_session() as s:
            res = await s.execute(
                select(UsersOrm).where(UsersOrm.tg_id == str(tg_id))
            )
            return res.scalar_one_or_none()

    @staticmethod
    async def update_user(tg_id: int, update_data: dict):
        """Обновляет данные пользователя"""
        async with async_session() as session:
            await session.execute(
                update(UsersOrm)
                .where(UsersOrm.tg_id == str(tg_id))
                .values(**update_data)
            )
            await session.commit()

    @staticmethod
    async def delete_user(tg_id: int) -> bool:
        async with async_session() as s:
            try:
                result = await s.execute(
                    delete(UsersOrm).where(UsersOrm.tg_id == str(tg_id))
                )
                await s.commit()
                return result.rowcount > 0  # True если пользователь был удален
            except SQLAlchemyError as e:
                await s.rollback()
                print(f"Ошибка при удалении пользователя: {e}")
                return False
