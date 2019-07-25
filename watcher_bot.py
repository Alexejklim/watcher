import logging
import json
import schedule
from aiogram import Bot, Dispatcher, executor
from timechecker import Today

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

if raspberry:
    from raspi_bot import Raspberry
    RPi = Raspberry(config['Raspberry'])
    
today = Today(config['Time'])

async def broadcaster():
    while True:
        schedule.run_pending()
        if raspberry:
            if watcherisrun and RPi.Muvement() and today.isBusinessday and today.isWorktime:
                await bot.send_photo(CHAT,RPi.Capture())
                # time.sleep(0.2)
                # await bot.send_message(CHAT, 'stream.getbuffer()')

if __name__ == '__main__':
    executor.start(dp, broadcaster())
