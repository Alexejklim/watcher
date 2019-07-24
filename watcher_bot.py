from io import BytesIO
import logging
import json
import schedule
from aiogram import Bot, Dispatcher, executor
import timechecker

config = {}
with open('config.conf', 'r') as configFile:
    config = json.load(configFile)

TOKEN = config['TOKEN']
CHAT = config['CHAT']

logging.basicConfig(level=logging.INFO)

raspberry = False
watcherisrun = True
isBusinessday = False

if raspberry:
    from raspi_bot import Raspberry
    RPi = Raspberry(config['Raspberry'])

bot = Bot(TOKEN)
dp = Dispatcher(bot)

async def broadcaster():
    while True:
        schedule.run_pending()
        isWorktime = time_in_range()
        stream = BytesIO()
        stream.seek(0)
        stream.truncate()
        if raspberry:
            if watcherisrun and RPi.Muvement() and isBusinessday and isWorktime:
                RPi.Capture(stream)
                await bot.send_photo(CHAT,stream.getbuffer())
                # time.sleep(0.2)
                # await bot.send_message(CHAT, 'stream.getbuffer()')

if __name__ == '__main__':
    executor.start(dp, broadcaster())