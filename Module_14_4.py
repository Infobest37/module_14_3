from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Исправлено
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db14_3 import *
import asyncio
import os
from crud_functions import is_included, add_user, initiate_db

api = "7945740698:AAEInDjzg83i0KA-71qopdj-KFwhISwCNvI"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text="Регистрация")
kb.add(button)

kb1 = ReplyKeyboardMarkup(resize_keyboard=True)  # resize_keyboard делает кнопки компактными
button1 = KeyboardButton(text="Рассчитать")
button_2 = KeyboardButton(text="Информация")
button_3 = KeyboardButton(text="Купить")
kb1.add(button, button_2)
kb1.add(button_3)

ikb = InlineKeyboardMarkup(row_width=1)
button_inline = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")
button_inline_2 = InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")
ikb.add(button_inline, button_inline_2)

product_buying = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Продукт 1", callback_data="product1")],
        [InlineKeyboardButton(text="Продукт 2", callback_data="product2")],
        [InlineKeyboardButton(text="Продукт 3", callback_data="product3")],
        [InlineKeyboardButton(text="Продукт 4", callback_data="product4")]
    ]
)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    user_name = State()
    emale = State()
    age = State()


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привет! Я бот, помогающий следить за здоровьем. Выберите действие:", reply_markup=kb)


@dp.message_handler(text="Регистрация")
async def sing_up(message: types.Message, state: FSMContext):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.user_name.set()


@dp.message_handler(state=RegistrationState.user_name)
async def set_username(message: types.Message, state: FSMContext):
    if is_included(message.text):
        await message.answer("Пользователь существует, введите другое имя")
        return
    await message.answer("Введите свой email:")
    await state.update_data(user_name=message.text)
    await RegistrationState.emale.set()


@dp.message_handler(state=RegistrationState.emale)
async def set_emale(message: types.Message, state: FSMContext):
    await message.answer("Введите свой возраст:")
    await state.update_data(emale=message.text)
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    await message.answer("Регистрация прошла успешно")
    data = await state.get_data()
    user_name = data["user_name"]
    emale = data["emale"]
    add_user(user_name, emale, message.text)
    await state.finish()


@dp.message_handler(text="Рассчитать")
async def main_menu(message: types.Message):
    """
    Обработчик кнопки 'Рассчитать' из Reply клавиатуры.
    """
    await message.answer("Выберите опцию:", reply_markup=ikb)


@dp.message_handler(text="Купить")
async def get_buying_list(message: types.Message):
    products = get_all_products()

    for title, description, price in products:
        # Формируем путь к изображению для каждого продукта
        photo_file = os.path.join("photo", f"{title}.jpg")  # ищем файл по названию

        if os.path.exists(photo_file):
            with open(photo_file, "rb") as image:
                await message.answer_photo(image, f"Название: {title} | Описание: {description} | Цена: {price}")
        else:
            await message.answer(f"Фотография для {title} не найдена.")

    await message.answer(text="Выберите продукт для покупки", reply_markup=product_buying)


@dp.callback_query_handler(text="product1")
async def product1(call):
    await call.message.answer("Вы успешно приобрели продукт")


@dp.callback_query_handler(text="product2")
async def product1(call):
    await call.message.answer("Вы успешно приобрели продукт")


@dp.callback_query_handler(text="product3")
async def product1(call):
    await call.message.answer("Вы успешно приобрели продукт")


@dp.callback_query_handler(text="product4")
async def product1(call):
    await call.message.answer("Вы успешно приобрели продукт")


@dp.callback_query_handler(text="calories")
async def set_age(call: types.CallbackQuery):
    """
    Начало машины состояний, обработка кнопки 'Рассчитать норму калорий'.
    """
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()
    await call.answer()


@dp.callback_query_handler(text="formulas")
async def formulas(call: types.CallbackQuery):
    formulas_text = (
        "Формула для мужчин: 10 × вес (кг) + 6.25 × рост (см) − 5 × возраст (г) + 5\n"
        "Формула для женщин: 10 × вес (кг) + 6.25 × рост (см) − 5 × возраст (г) − 161"
    )
    await call.message.answer(formulas_text)
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer("Введите свой рост (в см):")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    await message.answer("Введите свой вес (в кг):")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    age = data["age"]
    growth = data["growth"]
    weight = data["weight"]
    calories = 10 * weight + 6.25 * growth - 5 * age + 5  # Формула для мужчин (можно настроить)

    await message.answer(
        f"Ваши данные:\nВозраст: {age}\nРост: {growth} см\nВес: {weight} кг.\n"
        f"Ваша норма калорий: {calories:.2f} ккал. в сутки",
        reply_markup=kb  # Возвращаем клавиатуру
    )
    await state.finish()


@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def all_messages(message: types.Message):
    """
    Обработчик для всех остальных сообщений.
    """
    await message.answer("Я вас не понимаю. Пожалуйста, выберите действие с помощью кнопок.", reply_markup=kb)


if __name__ == '__main__':
    initiate_db()
    executor.start_polling(dp, skip_updates=True)
