from parsers import anime_bit
from service.alchemy import session, Sql_users, Sql_anime, Sql_anime_playlist, Sql_anime_urls, Sql_users_log
from service.logger import logger
from aiogram.types import Message
from datetime import datetime
from sqlalchemy import desc


async def get_user_by_t_id(telegram_id):
    return session.query(Sql_users).filter_by(telegram_id=telegram_id).first()


async def get_user_id_by_t_id(telegram_id):
    sql_user = session.query(Sql_users.id).filter_by(telegram_id=telegram_id).first()
    if sql_user is None:
        return None
    else:
        return sql_user[0]


async def get_anime_by_id(anime_id):
    return session.query(Sql_anime).filter(Sql_anime.id == anime_id).first()


async def get_anime_name_by_id(anime_id):
    return session.query(Sql_anime.name).filter_by(id=anime_id).first()


async def get_anime_playlists(user_id, anime_id=None):
    if anime_id is None:
        return session.query(Sql_anime_playlist).filter(Sql_anime_playlist.user_id == user_id, Sql_anime_playlist.state == 'watching').all()
    else:
        return session.query(Sql_anime_playlist).filter_by(user_id=user_id, anime_id=anime_id).first()


async def get_users_by_anime_in_playlist(new_series, anime_id):
    sql_users = session.query(Sql_users) \
        .join(Sql_anime_playlist).filter(Sql_anime_playlist.anime_id == anime_id, Sql_anime_playlist.series != new_series) \
        .all()
    return sql_users


async def get_subscribe_status(user_id, anime_id):
    sql_anime_playlist = session.query(Sql_anime_playlist).filter_by(anime_id=anime_id, user_id=user_id).first()
    if not sql_anime_playlist:
        await add_anime_to_playlist(user_id, anime_id)
        return 'added to db'

    if sql_anime_playlist.state == 'watching':
        sql_anime_playlist.state = 'drop'
    else:
        sql_anime_playlist.state = 'watching'

    session.commit()
    return sql_anime_playlist.state


async def add_anime_to_playlist(user_id, anime_id):
    new_anime_playlist = Sql_anime_playlist(
        user_id=user_id,
        anime_id=anime_id,
        series=1,
        state='watching'
    )
    session.add(new_anime_playlist)
    session.commit()

    return new_anime_playlist


async def get_users_with_subscription() -> Sql_users:
    return session.query(Sql_users).filter(Sql_users.subscription == True).all()


async def add_new_anime(name: str, season: int, series: int, last_series: int, year: int, genre: str, country: str, description: str, anime_type: str, image: str, more_series: bool, url: str):
    new_sql_anime = Sql_anime(name, season, series, last_series, year, genre, country, description, anime_type, image, more_series)
    session.add(new_sql_anime)
    session.commit()

    anime_url_in_db: Sql_anime_urls = session.query(Sql_anime_urls.id).filter(Sql_anime_urls.id == new_sql_anime.id).first()
    if not anime_url_in_db:
        session.add(Sql_anime_urls(
            anime_id=new_sql_anime.id,
            url=url,
        ))
    else:
        anime_url_in_db.anime_id = new_sql_anime
        anime_url_in_db.url = url

    session.commit()
    logger.info(f"Аниме добавлено в базу: '{name}' ")

    return new_sql_anime


async def get_anime_by_name(anime_name: str):
    return session.query(Sql_anime).filter(Sql_anime.name == anime_name).first()


async def get_user_and_add_log(message: Message):
    sql_user = await get_user_by_t_id(message.from_user.id)

    if not sql_user:
        sql_user = add_new_user(message)
    new_log = Sql_users_log(message.from_user.id, message.text)
    session.add(new_log)
    session.commit()
    return sql_user


async def add_new_user(message: Message):
    if await get_user_id_by_t_id(message.from_user.id):
        return

    new_user = Sql_users(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        language=message.from_user.language_code,
    )

    session.add(new_user)
    session.commit()

    return new_user


async def update_anime_series(sql_anime: Sql_anime, new_series: int):
    sql_anime.last_series = new_series
    sql_anime.last_update = datetime.now()
    session.commit()


async def set_playlist_series(user_id: int, anime_id: int, current_series: int):
    sql_playlist = session.query(Sql_anime_playlist).filter(Sql_anime_playlist.user_id == user_id, Sql_anime_playlist.anime_id == anime_id).first()

    if sql_playlist is None:
        await add_anime_to_playlist(user_id, anime_id)
        return 'added to db'

    sql_playlist.series = current_series
    session.commit()

    return await check_anime_state(current_series, anime_id)


async def check_anime_state(current_series, anime_id):
    anime_series, more_series = session.query(Sql_anime.series, Sql_anime.more_series).filter(Sql_anime.id == anime_id).first()

    if anime_series == current_series and not more_series:
        return 'finished'
    else:
        return 'watching'


async def get_anime_series(anime_id):
    return session.query(Sql_anime.series).filter(Sql_anime.id == anime_id).first()[0]


async def add_t_image_id(anime_id: int, t_image_id: str):
    sql_anime = session.query(Sql_anime).filter(Sql_anime.id == anime_id).first()
    sql_anime.t_image_id = t_image_id
    session.commit()


async def get_some_last_anime(count):
    return session.query(Sql_anime).order_by(desc(Sql_anime.last_update)).limit(count).all()


async def get_anime_by_url(url) -> Sql_anime:
    sql_anime = session.query(Sql_anime).join(Sql_anime_urls).filter(Sql_anime_urls.url == url).first()
    if sql_anime is None:
        sql_anime = await anime_bit.add_anime_to_db_from_anime_page(url)
    return sql_anime
