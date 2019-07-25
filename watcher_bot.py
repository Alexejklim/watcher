import logging
import json
from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
import schedule
from timecontroller import Today

config = {}
with open('config.conf', 'r') as configFile:
    config = json.load(configFile)

TOKEN = config['TOKEN']
CHAT = config['CHAT']

logging.basicConfig(level=logging.INFO)

raspberry = False
watcherisrun = True

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

@dp.message_handler(commands=['start'])
async def process_start(message: Message):
    await bot.send_message(message.from_user.id,"Привет!", reply_markup=main_keyboard)
    
if raspberry:
    from raspi_bot import Raspberry
    RPi = Raspberry(config['Raspberry'])
    
today = Today(config['Time'])

async def broadcaster():
    while True:
        schedule.run_pending()
        print('xxxxxxxxxxxxxx')
        if raspberry:
            if watcherisrun and RPi.Muvement() and today.isBusinessday and today.isWorktime:
                await bot.send_photo(CHAT,RPi.Capture())
                # time.sleep(0.2)
                # await bot.send_message(CHAT, 'stream.getbuffer()')

if __name__ == '__main__':
    executor.start_polling(dp)
    #executor.start(dp, broadcaster())

  


#schedule.every(period).seconds.(time_str).do(run_func)  
#schedule.clear()

#if flagpericdic and setperiod = everyminut:
#elif flagpericdic and setperiod = everyhour:


#2 enclosure : every 5 min, every 30 min, every hour, every 2 hour every 4 hour, every 6 hour every 12 hour ,every day , every 2 days
#2.1 set time default current
#3 stop security forever, if now stop, than run security
#4 sent fresh exchange at 14. in businessdays
#кнопки управления ботом...
