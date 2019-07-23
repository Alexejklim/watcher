from io import BytesIO
import logging
import json

raspberry = False

config = {}
with open('config.conf', 'r') as configFile:
    config = json.load(configFile)

if raspberry:
    from raspi_bot import Raspberry
    RPi = Raspberry(config['Raspberry'])

from aiogram import Bot, Dispatcher, executor
logging.basicConfig(level=logging.INFO)

TOKEN = config['TOKEN']
CHAT = config['CHAT']

bot = Bot(TOKEN)
dp = Dispatcher(bot)

async def broadcaster():
    print(config['TOKEN'])
    while True:
        stream = BytesIO()
        stream.seek(0)
        stream.truncate()
        if raspberry and RPi.Muvement():
            RPi.Capture(stream)
            await bot.send_photo(CHAT,stream.getbuffer())
            # time.sleep(0.2)
            # await bot.send_message(CHAT, 'stream.getbuffer()')

if __name__ == '__main__':
    executor.start(dp, broadcaster())