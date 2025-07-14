from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from database.queries.orm import Orm

router = Router()


@router.message(Command("profile"))
async def get_profile_info(message: Message):
    try:
        user = await Orm.get_user_by_tg_id(message.from_user.id)

        if not user:
            await message.answer(
                "Вы еще не заполняли форму, используйте /form"
            )
            return

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Удалить профиль", callback_data="delete_profile"
                    ),
                ]
            ]
        )

        profile_text = (
            "📌 Ваш профиль:\n\n"
            f"👤 Имя: {user.name}\n"
            f"🏙️ Город: {user.city}\n"
            f"🔢 Возраст: {user.age}\n"
            f"🚻 Пол: {user.gender}\n"
            f"📱 Телефон: {user.phone_number}\n"
            f"👾 Username: {user.username if user.username else 'не указан'}"
        )

        await message.answer(profile_text, reply_markup=keyboard)

    except Exception as e:
        await message.answer("Ошибка при загрузке профиля")
        print(f"Error loading profile: {e}")


@router.callback_query(F.data == "delete_profile")
async def delete_profile(callback: CallbackQuery):
    deleted = await Orm.delete_user(callback.from_user.id)

    if deleted:
        await callback.message.answer("Ваши данные были удалены")
    else:
        await callback.message.answer(
            "Ваши данные не были найдены или произошла ошибка"
        )

    await callback.answer()
