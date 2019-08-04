import logging, json, asyncio
from aiogram import Bot, Dispatcher, executor, filters
from aiogram.types import Message, CallbackQuery
from timecontroller import Today
from raspberry import Raspberry
from keyboard import keyboard
from states import watcher, periodic

with open('private_config.conf', 'r') as configFile:
    config = json.load(configFile)

TOKEN, CHAT = config['TOKEN'], config['CHAT']

with open('config.conf', 'r') as configFile:
    config = json.load(configFile)

LOOP_DELAY, Timelist =  config['DELAY'], config['Timelist']

logging.basicConfig(level=logging.INFO)
today = Today(config['Time'])
Raspberry = Raspberry(config['Raspberry'])
watcher = watcher()
periodic = periodic()
keyboard = keyboard(watcher,periodic,Timelist)
bot = Bot(TOKEN)
dp = Dispatcher(bot)
loop = asyncio.get_event_loop()

def repeat(wrapped):
    def wrapper():
        loop.call_later(wrapped(), wrapper)
    return wrapper


async def send_photo(chat):
    await bot.send_photo(chat,Raspberry.Capture())


async def edit_message(message, callback_query):
    await bot.edit_message_text(message
                                , callback_query.from_user.id
                                , callback_query.message.message_id
                                , reply_markup=keyboard.main_keyboard)


@repeat
def watcher_photos():
    if Raspberry.Isrun and watcher.Isrun and today.Isbusinessday() and today.Isworktime() and Raspberry.Muvement():
        loop.create_task(send_photo(CHAT))
    return LOOP_DELAY

@repeat
def periodic_photos():
    if Raspberry.Isrun and periodic.Isrun:
        loop.create_task(send_photo(CHAT))
    return periodic.period


@dp.message_handler(filters.CommandStart())
async def process_start(message: Message):
    await bot.send_message(message.from_user.id
                           , "Hi! What do you want to do?"
                           , reply_markup=keyboard.main_keyboard)


@dp.callback_query_handler(lambda command: command.data == 'make_photo')
async def callback_make_photo(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if Raspberry.Isrun:
        await send_photo(callback_query.from_user.id)
        await edit_message("Anything else?", callback_query)
    else:
        await edit_message("Access to the camera is forbidden.Anything else?", callback_query)


@dp.callback_query_handler(lambda command: command.data == 'periodic_photo')
async def callback_watcher(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if not Raspberry.Isrun:
        await edit_message("Access to the camera is forbidden.Anything else?", callback_query)
    else:
        if not periodic.Isrun:
            periodic.message = 'Please set time for cycle. Default 5 seconds'
        periodic.switch()
        keyboard.update()
        await edit_message(periodic.message, callback_query)


@dp.callback_query_handler(lambda command: command.data in Timelist)
async def callback_watcher(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    periodic.set_period(Timelist[callback_query.data])
    await edit_message("Now period is " + callback_query.data, callback_query)


@dp.callback_query_handler(lambda command: command.data == 'switch_watcher')
async def callback_watcher(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if not Raspberry.Isrun:
        await edit_message("Access to the camera is forbidden.Anything else?", callback_query)
    else:
        watcher.switch()
        keyboard.update()
        await edit_message(watcher.message, callback_query)


if __name__ == '__main__':
    loop.call_soon(watcher_photos)
    loop.call_soon(periodic_photos)
    executor.start_polling(dp, loop=loop)

