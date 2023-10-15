from aiogram import types
from service import sql


async def get_post_keyboard(sql_anime):
    keyboard = types.InlineKeyboardMarkup()

    watched = types.InlineKeyboardButton(text='Просмотрел!', callback_data=f'anime_post_watched_{sql_anime.id}')
    link = types.InlineKeyboardButton(text='Ссылка!', url=sql_anime.anime_urls[0].url)

    settings = types.InlineKeyboardButton(text='...', callback_data=f"settings_{sql_anime.id}")

    keyboard.row(watched)
    keyboard.row(link)
    keyboard.row(settings)

    return keyboard


async def get_main_keyboard(message: types.Message):
    button_menu = types.ReplyKeyboardMarkup(resize_keyboard=False)
    button_menu.add(types.InlineKeyboardButton("Найти аниме"))
    button_menu.add(types.InlineKeyboardButton("Мой плейлист"))
    button_menu.add(types.InlineKeyboardButton("Настройки"))
    button_menu.add(types.InlineKeyboardButton("Закрыть"))

    await message.answer("Главное меню:", reply_markup=button_menu)


async def get_post_settings(message: types.Message, anime_id: int):
    sql_anime = await sql.get_anime_by_id(anime_id)
    user_id = await sql.get_user_id_by_t_id(message.chat.id)

    keyboard = types.InlineKeyboardMarkup()

    subscribe_status = await get_subscribe_status(user_id, anime_id)

    keyboard.row(types.InlineKeyboardButton(text=subscribe_status, callback_data=f'anime_post_subscribe_{sql_anime.id}'))
    keyboard.row(types.InlineKeyboardButton(text='Указать кол-во просмотренных серий', callback_data=f'anime_post_set_series_{sql_anime.id}'))
    keyboard.row(types.InlineKeyboardButton(text='Назад', callback_data=f"anime_post_back_{sql_anime.id}"))

    return keyboard


async def get_subscribe_status(user_id, anime_id):
    sql_playlist = await sql.get_anime_playlists(user_id, anime_id)

    if sql_playlist is None or sql_playlist.state == 'drop':
        return 'Отслеживать'
    else:
        return 'Не отслеживать'
