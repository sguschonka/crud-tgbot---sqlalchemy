from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}\nЯ тестовый бот, реализующий CRUD(Создание, чтение, обновление и удаление данных с базы данных PostgreSQL)\n Начнем работу?\nОтправь /form"
    )
