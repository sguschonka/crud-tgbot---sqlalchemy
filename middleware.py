import logging
from collections.abc import Awaitable, Callable
from logging.handlers import RotatingFileHandler
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject


# Настройка логгера с гарантированной UTF-8 кодировкой
def setup_middleware_logger():
    logger = logging.getLogger("bot_middleware")

    # Очищаем предыдущие обработчики (если есть)
    if logger.handlers:
        logger.handlers.clear()

    # Создаем обработчик с явным указанием UTF-8
    handler = RotatingFileHandler(
        "logs.txt",
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8",
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(log_type)s | User %(user_id)s: %(log_content)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    return logger


middleware_logger = setup_middleware_logger()


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        try:
            user_id = event.from_user.id
            if isinstance(event, Message):
                log_content = event.text or str(event.content_type)
                middleware_logger.info(
                    "",
                    extra={
                        "log_type": "Message",
                        "user_id": user_id,
                        "log_content": log_content,
                    },
                )
            elif isinstance(event, CallbackQuery):
                middleware_logger.info(
                    "",
                    extra={
                        "log_type": "Callback",
                        "user_id": user_id,
                        "log_content": event.data,
                    },
                )
        except Exception as e:
            middleware_logger.error(f"Logging error: {str(e)}")

        return await handler(event, data)
