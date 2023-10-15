from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from service import sql
from telegram.loader import bot, dp
from telegram.handler import states
from aiogram import types
from service.logger import logger
from service import images

anime_id_whose_questing = {}


async def find_users_and_send_post_to_tg(new_series, sql_anime):

    sql_users = await sql.get_users_by_anime_in_playlist(new_series, sql_anime.id)

    for sql_user in sql_users:
        sql_playlist = sql.get_anime_playlists(sql_user.id, sql_anime.id)
        await send_anime_post(sql_anime, sql_user.telegram_id, sql_playlist)


async def send_anime_post(sql_anime: sql.Sql_anime, telegram_id, sql_playlist: sql.Sql_anime_playlist= None):

    if isinstance(sql_anime, int):
        sql_anime = await sql.get_anime_by_id(sql_anime)

    if sql_anime.t_image_id is None:
        exist_t_image_id = False
    else:
        exist_t_image_id = True

    keyboard = await post_keyboard(sql_anime, sql_playlist)

    if sql_playlist:
        text = f"{sql_anime.name}:\nПросмотрено: {sql_playlist.series}  из {sql_anime.last_series} (Всего {sql_anime.series})"
    else:
        text = f"{sql_anime.name}:\nВышло: {sql_anime.last_series} из {sql_anime.series}"

    # try:
    if exist_t_image_id:
        if sql_anime.image[-4:] == 'webp': #TODO ломается при  https://anime-bit.ru/content/6112/ ссылке
            await bot.send_sticker(
                    telegram_id,
                    sql_anime.t_image_id,
                    disable_notification=True,
            )
        else:
            await bot.send_photo(
                    telegram_id,
                    sql_anime.t_image_id,
                    disable_notification=True,
            )
    else:
        if sql_anime.image[-4:] == 'webp':
            msg = await bot.send_sticker(
                    telegram_id,
                    sql_anime.image,
                    disable_notification=True,
            )

            await sql.add_t_image_id(sql_anime.id, msg.sticker.file_id)
        else:
            bio_image = images.change_image_size(sql_anime.image)
            msg = await bot.send_photo(
                    telegram_id,
                    bio_image,
                    disable_notification=True,
            )
            await sql.add_t_image_id(sql_anime.id, msg.photo.file_id)
    await bot.send_message(
            telegram_id,
            text,
            reply_markup=keyboard,
            disable_notification=True
    )
    # except Exception:
    #     logger.error(f'Не удалось отправить ответ для {telegram_id}')


async def post_keyboard(sql_anime, sql_playlist):
    keyboard = InlineKeyboardMarkup().add()

    watched = InlineKeyboardButton(text='Просмотрел!', callback_data=f'anime_post_watched_{sql_anime.id}')
    link = InlineKeyboardButton(text='Ссылка!', url=sql_anime.anime_urls[0].url)

    if sql_playlist is None or sql_playlist.state == 'drop':
        subscribe_status = 'Отслеживать'
    else:
        subscribe_status = 'Не отслеживать'

    settings = InlineKeyboardButton(text=subscribe_status, callback_data=f'anime_post_subscribe_{sql_anime.id}')

    keyboard.row(watched)
    keyboard.row(link)
    keyboard.row(settings)

    return keyboard


@dp.callback_query_handler(lambda c: "anime_post_watched_" in c.data)
async def anime_post_watched_(callback_query: types.CallbackQuery):
    anime_id = int(callback_query.data.split('_')[-1])
    watched_series = int(callback_query.message.text.split(' ')[-3])
    user_t_id = callback_query.from_user.id
    user_id = await sql.get_user_id_by_t_id(user_t_id)
    anime_state = await sql.set_playlist_series(user_id, anime_id, watched_series)

    if anime_state == 'added to db':
        await dp.current_state(user=user_t_id).set_state(states.Questions.how_many_series_user_watch)
        anime_id_whose_questing[user_id] = anime_id
        await bot.send_message(user_t_id, 'Аниме добавленно в плейлист!\nСколько вы просмотрели?')
    else:
        sql_anime = await sql.get_anime_by_id(anime_id)

        if anime_state == 'watching':
            await bot.send_message(user_t_id, f'{sql_anime.name}\nПросмотренно {watched_series} из {sql_anime.series}', disable_notification=True)

        elif anime_state == 'finished':
            await bot.send_message(user_t_id, f'{sql_anime.name}\nВсё просмотренно {watched_series} из {sql_anime.series}!', disable_notification=True)

    await bot.answer_callback_query(callback_query.id)


@dp.message_handler(state=states.Questions.how_many_series_user_watch)
async def first_test_state_case_met(message: types.Message):
    text = message.text
    user_t_id = message.from_user.id
    user_id = await sql.get_user_id_by_t_id(user_t_id)

    if text.isnumeric():
        anime_id = anime_id_whose_questing[user_id]
        await sql.set_playlist_series(user_id, anime_id, int(text))

        del anime_id_whose_questing[user_id]
        await dp.current_state(user=user_t_id).reset_state()

    elif text.lower() == 'отмена':
        await dp.current_state(user=user_t_id).reset_state()
        del anime_id_whose_questing[user_id]
        await message.reply('Ну и ладна!', reply=False)
    else:
        await message.reply('Я тебя не понимаю :с\nЕсли не хотите отвечать, то напишете "Отмена"')


@dp.callback_query_handler(lambda c: "anime_post_subscribe_" in c.data)
async def anime_post_subscribe_(callback_query: types.CallbackQuery):
    user_t_id = callback_query.from_user.id
    user_id = await sql.get_user_id_by_t_id(user_t_id)
    anime_id = int(callback_query.data.split('_')[-1])

    status = await sql.subscribe_or_unsubscribe_to_anime(user_id, anime_id)
    if status == 'added to db':
        anime_id_whose_questing[user_id] = anime_id
        await dp.current_state(user=user_t_id).set_state(states.Questions.how_many_series_user_watch)
        await bot.send_message(user_t_id, 'Аниме добавленно в плейлист!\nСколько вы просмотрели?')
    elif status == 'watching':
        await bot.send_message(user_t_id, 'Вы подписались на рассылку')
    elif status == 'drop':
        await bot.send_message(user_t_id, 'Вы отписались от рассылки')
    await bot.answer_callback_query(callback_query.id)


