from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardButton
from service import sql
from telegram import anime_posts
from telegram.loader import dp


@dp.message_handler(text=['Найти аниме'])
async def start(message: Message):
    await find_last_anime_in_bd(message, 10)


# async def start( message: Message ):
#     button_menu = ReplyKeyboardMarkup(resize_keyboard = False)
#     button_menu.add(InlineKeyboardButton("Найти аниме"))
#     button_menu.add(InlineKeyboardButton('Показать 10 новых аниме'))
#
#     await message.answer("Найти аниме:", reply_markup = button_menu)
#


async def find_last_anime_in_bd(message: Message, count):
    last_some_anime = await sql.get_some_last_anime(count)
    for sql_anime in last_some_anime:
        await anime_posts.send_anime_post(sql_anime, message.from_user.id)
