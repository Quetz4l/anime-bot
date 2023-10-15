from telegram.handler import states
from telegram.handler.keyboards import anime_id_whose_questing
from service import sql
from telegram.loader import bot, dp

async def subscribe(user_t_id, anime_id):
    sql_anime = await sql.get_anime_by_id(anime_id)
    user_id = await sql.get_user_id_by_t_id(user_t_id)
    status = await sql.get_subscribe_status(user_id, anime_id)

    if status == 'added to db':
        anime_id_whose_questing[user_id] = anime_id
        await dp.current_state(user=user_t_id).set_state(states.Questions.how_many_series_user_watch)
        await bot.send_message(user_t_id, 'Аниме добавленно в плейлист!\nСколько вы просмотрели?')
        return True
    elif status == 'watching':
        await bot.send_message(user_t_id, f'Вы подписались на {sql_anime.name}')
        return True
    elif status == 'drop':
        await bot.send_message(user_t_id, f'Вы отписались от {sql_anime.name}')
        return True
    else: return False