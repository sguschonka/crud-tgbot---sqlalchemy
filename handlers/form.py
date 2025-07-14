import phonenumbers
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from phonenumbers.phonenumberutil import NumberParseException

from database.queries.orm import Orm

router = Router()


class Form(StatesGroup):
    name = State()
    age = State()
    phone_number = State()
    gender = State()
    city = State()


@router.message(Command("form"))
async def start_form(message: Message, state: FSMContext):
    await message.answer("Введите ваше имя:")
    await state.set_state(Form.name)


@router.message(Form.name)
async def name_processing(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.phone_number)
    await message.answer("Хорошо, теперь введите Ваш номер телефона")


@router.message(Form.phone_number)
async def phone_processing(message: Message, state: FSMContext):
    phone_text = message.text.strip()
    try:
        p = phonenumbers.parse(phone_text, "RU")
        if not phonenumbers.is_valid_number(p):
            raise ValueError
        formatted_p = phonenumbers.format_number(
            p, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )
        await state.update_data(phone_number=formatted_p)
        await state.set_state(Form.age)
        await message.answer(
            "Номер телефона принят! Теперь введите Ваш возраст"
        )
    except (NumberParseException, ValueError):
        await message.answer(
            "🚫 Неверно указан номер телефона!\nПример: +79161234567 или 89651234567"
        )
        return


@router.message(Form.age)
async def age_processing(message: Message, state: FSMContext):
    age = message.text
    try:
        if not (1 <= int(age) <= 120):
            raise ValueError
        await state.update_data(age=message.text)
        await state.set_state(Form.gender)
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Мужской", callback_data="gender_male"
                    ),
                    InlineKeyboardButton(
                        text="Женский", callback_data="gender_female"
                    ),
                ]
            ]
        )
        await message.answer("Какого вы пола?", reply_markup=keyboard)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный возраст (1-120)")


@router.callback_query(F.data == "gender_male")
async def gender_male(callback: CallbackQuery, state: FSMContext):
    await state.update_data(gender="Мужской")
    await state.set_state(Form.city)
    await callback.message.answer("Введите ваш город")
    await callback.answer()


@router.callback_query(F.data == "gender_female")
async def gender_female(callback: CallbackQuery, state: FSMContext):
    await state.update_data(gender="Женский")
    await state.set_state(Form.city)
    await callback.message.answer("Введите ваш город")
    await callback.answer()


@router.message(Form.city)
async def continue_form(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    data = await state.get_data()
    name = data.get("name")
    phone_number = data.get("phone_number")
    age = data.get("age")
    gender = data.get("gender")
    city = data.get("city")
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Подтвердить", callback_data="confirm_form"
                ),
                InlineKeyboardButton(
                    text="Отменить", callback_data="cancel_form"
                ),
            ]
        ]
    )
    await message.answer(
        f"Проверьте введённые данные\n\nИмя: {name}\nТелефон: {phone_number}\nВозраст: {age}\nГород: {city}\nПол: {gender}",
        reply_markup=keyboard,
    )


@router.callback_query(F.data == "confirm_form")
async def save_form(callback: CallbackQuery, state: FSMContext):
    user_tg_id = callback.from_user.id
    user_data = await state.get_data()

    database_data = {
        "tg_id": str(callback.from_user.id),
        "name": user_data.get("name"),
        "city": user_data.get("city"),
        "age": int(user_data.get("age")),
        "gender": user_data.get("gender"),
        "phone_number": user_data.get("phone_number"),
        "username": f" @{str(callback.from_user.username)}",
    }

    try:
        user = await Orm.get_user_by_tg_id(user_tg_id)

        if user:
            await Orm.update_user(user_tg_id, database_data)
            await callback.message.answer("Данные успешно обновлены!")
        else:
            await Orm.insert_user(database_data)
            await callback.message.answer("Данные успешно сохранены!")
    except Exception as e:
        await callback.message.answer(f"Произошла ошибка: {str(e)}")
        print(f"Error saving user data: {e}")

    await callback.answer()
    await state.clear()


@router.callback_query(F.data == "cancel_form")
async def delete_form(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Форма отменена!")
    await callback.answer()
    await state.clear()
