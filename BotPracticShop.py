import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Исправлено
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
from config import *
from keybords import *
import text
from admin import *
import bd

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())  # Исправлено

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f"Добро пожаловать {message.from_user.username}" +text.start, reply_markup=start_kb)
#messege.answer_photo
@dp.message_handler(text='О нас')
async def info(message: types.Message):
   await message.answer(text.other, reply_markup=start_kb)
@dp.message_handler(text= "Стоимость")
async def price(message: types.Message):
   await message.answer("Какая игра вам интересна?", reply_markup= catalog_kb)
@dp.callback_query_handler(text="medium")
async def bayM(call):
    with open("photo/Product2.jpg", "rb") as f:
        await call.message.answer_photo(f, text.Mgame, reply_markup=buy_kb)
        await call.answer()
@dp.callback_query_handler(text="big")
async def bayL(call):
    with open("photo/Product3.jpg", "rb") as f:
        await call.message.answer_photo(f, text.Lgame, reply_markup=buy_kb)
        await call.answer()
@dp.callback_query_handler(text="mega")
async def bayXL (call):
    with open("photo/Product4.jpg", "rb") as f:
        await call.message.answer_photo(f, text.Xgame, reply_markup=buy_kb)
        await call.answer()
@dp.callback_query_handler(text="other")
async def other(call):
    with open("photo/Product2.jpg", "rb") as f:
        await call.message.answer(f, text.other, reply_markup=buy_kb)
        await call.answer()
@dp.callback_query_handler(text="back")
async def back(call):
    await call.message.answer("Какая игра вам интересна?", reply_markup= catalog_kb)
    await call.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
