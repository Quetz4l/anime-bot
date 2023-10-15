from aiogram import types
from telegram.loader import dp
from aiogram.types import Message
from telegram.keyboard import find_anime


async def start( message: types.Message ):
    button_menu = types.ReplyKeyboardMarkup(resize_keyboard = False)
    button_menu.add(types.InlineKeyboardButton("Найти аниме"))
    button_menu.add(types.InlineKeyboardButton("Мой плейлист"))
    button_menu.add(types.InlineKeyboardButton("Настройки"))

    await message.answer("Главное меню:", reply_markup = button_menu)



@dp.message_handler(commands=['Найти аниме'])
async def hello(message: Message):
    await find_anime.start(message)



@dp.message_handler(commands=['Мой плейлист'])
async def hello(message: Message):
    await find_anime.start(message)



@dp.message_handler(commands=['Настройки'])
async def hello(message: Message):
    await find_anime.start(message)








