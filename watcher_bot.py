import logging, json, asyncio
from aiogram import Bot, Dispatcher, executor, filters
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from timecontroller import Today

config = {}
with open('config.conf', 'r') as configFile:
    config = json.load(configFile)

TOKEN = config['TOKEN']
CHAT = config['CHAT']

logging.basicConfig(level=logging.INFO)

raspberry = True
watcherisrun = True

if raspberry:
    from raspi_bot import Raspberry
    RPi = Raspberry(config['Raspberry'])

bot = Bot(TOKEN)
dp = Dispatcher(bot)

make_photo = InlineKeyboardButton('/make_photo',callback_data='make_photo')
periodic_photo = InlineKeyboardButton('/periodic_photo',callback_data='periodic_photo')
watcher_settings = InlineKeyboardButton('/watcher_settings',callback_data='watcher_settings')
main_keyboard = InlineKeyboardMarkup()
main_keyboard.add(make_photo,periodic_photo,watcher_settings)

@dp.callback_query_handler(lambda c: c.data == 'make_photo')
async def callback_make_photo(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if raspberry:
        await bot.send_photo(callback_query.from_user.id,RPi.Capture())
    else: 
        await bot.send_message(callback_query.from_user.id, 'Access to the camera is forbidden')

@dp.message_handler(filters.CommandStart())
async def process_start(message: Message):
    await bot.send_message(message.from_user.id,"Привет!", reply_markup=main_keyboard)

    
today = Today(config['Time'])

async def broadcaster():
    if raspberry:
        if watcherisrun and RPi.Muvement() and today.isBusinessday and today.isWorktime:
            await bot.send_photo(CHAT,RPi.Capture())

def repeat(loop):
    loop.create_task(broadcaster())
    loop.call_later(5, repeat, loop)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.call_soon(repeat, loop)
    executor.start_polling(dp, loop=loop)

