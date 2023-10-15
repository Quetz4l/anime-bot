from telegram.loader import dp, types
from service import utils, sql


@dp.message_handler(lambda text: 'anime-bit.ru' in text.text)
async def parse_anime_bit_handler(message: types.Message):
    t_user_id = message.from_user.id
    sql_anime = await sql.get_anime_by_url(message.text)
    if sql_anime is False or await utils.subscribe(t_user_id, sql_anime.id ) is False:
        await message.reply('Ссылка точно правильная?')