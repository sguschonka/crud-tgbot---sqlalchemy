import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from config import BOT_TOKEN
from handlers import routers
from middleware import LoggingMiddleware

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.message.middleware(LoggingMiddleware())
for router in routers:
    dp.include_router(router)


async def set_main_menu(bot):
    await bot.set_my_commands(
        [
            BotCommand(command="/start", description="Запустить бота"),
            BotCommand(command="/form", description="Собрать форму"),
            BotCommand(command="/profile", description="Показать профиль"),
        ]
    )


async def main():
    await set_main_menu(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
