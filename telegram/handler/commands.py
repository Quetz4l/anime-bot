from aiogram import types
from service import sql
from telegram.loader import dp

# cl_anime_post = CallbackData('anime_post', 'anime_id', 'action', 'value')

#
# @dp.callback_query_handler(send_posts.cl_anime_settings.filter(action='hidden_anime_settings'))
# async def call_back_anime_subscribe(callback_query: CallbackQuery, callback_data: dict):
#     sql_anime = await sql.get_anime_by_anime_id(callback_data['anime_id'])
#     sql_user = await sql.get_user_by_telegram_id(callback_query.from_user.id)
#     keyboard = await get_anime_settings(sql_anime, sql_user)
#
#     await bot.edit_message_reply_markup(
#             callback_query.from_user.id,
#             callback_query.message.message_id,
#             reply_markup=keyboard
#     )


# @dp.callback_query_handler(cl_anime_post.filter(action='anime_subscribe/unsubscribe'))
# async def call_back_anime_subscribe(callback_query: CallbackQuery, callback_data: dict):
#     t_user_id = callback_query.from_user.id
#     sql_user = await sql.get_user_by_telegram_id(t_user_id)
#     user_id = sql_user.id
#     anime_id = int(callback_data['anime_id'])
#
#     sql_anime_playlist = await sql.get_anime_playlist_by_user_id_and_anime_id(user_id, anime_id)
#     sql_anime = await sql.get_anime_by_anime_id(anime_id)
#
#     if sql_anime_playlist:
#         is_subscribe = sql_anime_playlist.subscribe
#     else:
#         await sql.add_anime_to_playlist(sql_user, sql_anime)
#         is_subscribe = False
#
#     if is_subscribe:
#         new_subscribe_state = False
#     else:
#         new_subscribe_state = True
#
#     await sql.subscribe_or_unsubscribe_to_anime(
#             t_user_id,
#             anime_id,
#             new_subscribe_state
#     )
#
#     await bot.edit_message_reply_markup(
#             t_user_id,
#             callback_query.message.message_id,
#             reply_markup=await send_posts.get_buttons(sql_anime)
#     )
#
#
#     if new_subscribe_state:
#         await bot.send_message(callback_query.from_user.id, f'Вы подписались на {sql_anime.name}')
#     else:
#         await bot.send_message(callback_query.from_user.id, f'Вы отписались от {sql_anime.name}')
#
# @dp.callback_query_handler(cl_anime_post.filter(action='close_menu'))
# async def call_back_anime_close_menu(callback_query: CallbackQuery, callback_data:dict):
#     sql_anime = await sql.get_anime_by_anime_id(callback_data['anime_id'])
#     await bot.edit_message_reply_markup(
#             callback_query.from_user.id,
#             callback_query.message.message_id,
#             reply_markup=await send_posts.get_buttons(sql_anime)
#     )
#
#
# async def get_anime_settings(sql_anime, sql_user):
#     sql_play_list = session.query(Sql_anime_playlist).filter_by(user_id=sql_user.id, anime_id=sql_anime.id).first()
#     if sql_play_list and sql_play_list.subscribe == True:
#         b_subscribe = InlineKeyboardButton(text='Отписаться от аниме', callback_data=cl_anime_post.new( anime_id=sql_anime.id, action='anime_subscribe/unsubscribe', value='unsubscribe'))
#     else:
#         b_subscribe = InlineKeyboardButton(text='Подписаться на аниме', callback_data=cl_anime_post.new( anime_id=sql_anime.id, action='anime_subscribe/unsubscribe', value='subscribe'))
#
#     b_close = InlineKeyboardButton(text="Закрыть", callback_data=cl_anime_post.new(anime_id=sql_anime.id, action='close_menu', value='close'))
#
#     b_settings = InlineKeyboardMarkup(resize_keyboard=False)
#     b_settings.add(b_subscribe)
#     b_settings.add(b_close)
#
#     return b_settings


"""Commands"""


# Команда подписки
@dp.message_handler(commands=['hello', 'hi', 'привет'])
async def hello(message: types.Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await sql.add_new_user(message)
    await message.answer('Нья !')


"""Utils"""


# Ответ на неузнанную команду
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer('Нья ?')
