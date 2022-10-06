from youtube_search import YoutubeSearch
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle
import hashlib
from scrapimdb import ImdbSpider
from Config import TOKEN


def get_info(name_1):
    im = ImdbSpider(name_1)
    a = im.get_rating()
    b = im.get_original_title()
    c = im.get_year()
    return a, b, c




def Searcher(text):
    results = YoutubeSearch(text, max_results=10).to_dict()
    return results




bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.inline_handler()
async def inline_handler(query : types.InlineQuery):       # Inline.Query - внутренние запросы
    text = query.query or 'echo'
    links = Searcher(text)

    articles = [types.InlineQueryResultArticle(
        id = hashlib.md5(f'{link["id"]}'.encode()).hexdigest(),      # hexdigest()   -
        title = f'{link["title"]}',
        url = f'https://www.youtube.com/watch?v={link["id"]}',
        thumb_url = f'{link["thumbnails"][0]}',
        input_message_content=types.InputTextMessageContent(
            message_text=f'https://www.youtube.com/watch?v={link["id"]}')
    ) for link in links]

    await query.answer(articles, cache_time=60, is_personal=True)





@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.message):
    await message.reply('Выберите язык info_ru!\nChoose language! info_en')
        #('Привет!\nЯ парсер бот, работающий в инлайн режиме!\nДля моего использования просто укажи @Utube_search_bot и напиши запрос..')


@dp.message_handler(commands=['info_ru'])
async def RU_info(message: types.message):
    await message.reply('Привет!\nЯ парсер бот, работающий в инлайн режиме!\nДля моего использования просто укажи @Utube_search_bot и напиши запрос..\n Помимо этого я также могу показать информацию о рейтинге, оригинальном названии и годе выхода фильма с IMDB по его названию!')


@dp.message_handler(commands=['info_en'])
async def EN_info(message: types.message):
    await message.reply('Not available yet!')


@dp.message_handler()
async def send_info(message: types.Message):

    await message.reply(get_info(message.text))


executor.start_polling(dp, skip_updates=True)















