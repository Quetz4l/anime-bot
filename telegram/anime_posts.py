from service import sql
from service.alchemy import Sql_users, Sql_anime
from telegram.loader import bot
from service import images, logger
from telegram.keyboard import keyboards
from aiogram.utils.exceptions import WrongFileIdentifier


async def find_users_and_send_post_to_tg(new_series, sql_anime):
    sql_users = await sql.get_users_by_anime_in_playlist(new_series, sql_anime.id)

    for sql_user in sql_users:
        sql_playlist = await sql.get_anime_playlists(sql_user.id, sql_anime.id)
        await send_anime_post(sql_anime, sql_user.telegram_id, sql_playlist)

async def send_new_anime_post(sql_anime: Sql_anime):
    sql_users: [Sql_users] = await sql.get_users_with_subscription()
    for sql_user in sql_users:
        await send_anime_post(sql_anime.id, sql_user.telegram_id)


async def send_anime_post(sql_anime: sql.Sql_anime, telegram_id, sql_playlist: sql.Sql_anime_playlist = None):
    if isinstance(sql_anime, int):
        sql_anime = await sql.get_anime_by_id(sql_anime)

    keyboard = await keyboards.get_post_keyboard(sql_anime)

    if sql_playlist:
        text = f"{sql_anime.name}:\nПросмотрено: {sql_playlist.series}  из {sql_anime.last_series} (Всего {sql_anime.series})"
    else:
        text = f"{sql_anime.name}:\nВышло: {sql_anime.last_series} из {sql_anime.series}"


    await send_img(sql_anime, telegram_id, text, keyboard)



async def send_img(sql_anime, telegram_id, caption, keyboard):

    if sql_anime.t_image_id is None or sql_anime.t_image_id == '':
        image = await images.default_converting(url=sql_anime.image)
    else:
        image = sql_anime.t_image_id

    await bot.send_photo(
            telegram_id,
            image,
            caption= caption,
            disable_notification= True,
            reply_markup=keyboard
    )