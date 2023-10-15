from aiogram.types import Message
from telegram.loader import dp
from telegram import anime_posts
from service import sql


@dp.message_handler(text=['Мой плейлист'])
async def show_my_playlist(message: Message):
    user_t_id = message.from_user.id
    user_id = await  sql.get_user_id_by_t_id(user_t_id)
    sql_playlists = await sql.get_anime_playlists(user_id)

    if sql_playlists is None:
        await message.reply('Ваш плейлист пуст :с', reply=False)

    for sql_playlist in sql_playlists:
        sql_anime = await sql.get_anime_by_id(sql_playlist.anime_id)
        await anime_posts.send_anime_post(sql_anime, user_t_id, sql_playlist)
