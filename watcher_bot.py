from io import BytesIO
import time, logging

raspberry = False

if raspberry:
    from raspi_tools import Raspberry
    RPi = Raspberry()
    stream = BytesIO()

from aiogram import Bot, Dispatcher, executor
logging.basicConfig(level=logging.INFO)

with open('TOKEN', 'r') as tokenfile:
   TOKEN = tokenfile.read()
with open('CHAT', 'r') as chatfile:
   CHAT = chatfile.read()


bot = Bot(TOKEN)
dp = Dispatcher(bot)

async def broadcaster():
    while True:
        if raspberry and RPi.Muvement():
            RPi.Capture(stream)
            await bot.send_photo(CHAT,stream.getbuffer())
            time.sleep(2)
            # await bot.send_message(CHAT, 'stream.getbuffer()')

if __name__ == '__main__':
    executor.start(dp, broadcaster())


# if flagsecurity and event and day is business and time is between(10:17):
# run
#if flagpericdic and setperiod = everyminut:
#elif flagpericdic and setperiod = everyhour:

#message start -keyboard with 1. make photo, 2.set periodic, 3.stop security 1 time , 3.security settings
#2 enclosure : every 5 min, every 30 min, every hour, every 2 hour every 4 hour, every 6 hour every 12 hour ,every day , every 2 days
#2.1 set time default current
#3 stop security forever, if now stop, than run security
#4 sent fresh exchange at 14. in businessdays
#кнопки управления ботом...
# модульная архитектура, отдельно бот,   отдельно камера(мб вынести камеру),отдельно функционал по курсам, отдельно скайсканнер..
# В телеграм бота встроить советчика по тому, в какую валюту лучше вкидываться на 10 день месяца...получить текущие курсы бгпб и мтбанка...
# ежедневно в 2 часа динамику к вчера, 10 числа или последний будний перед лучшую валюту для хранения...(берем курсы за последние 3 года,
# находим мин, макс, находим какую часть от мин макс составляет текущий, сравниваем, по доле, выбираем самую дешевую валюту,
# анализируем ,как сильно отличается сейчас курс в банке , где есть карточка, если все 3 валюты 30 % от максимума
# (т.е. бел рубль подешевел до 2.15 за доллар, 2.45 за евро  ), рекомендовать вклады в бел рублях....
# https://www.mtbank.by/currxml.php?d=23.07.2019
# http://www.nbrb.by/API/ExRates/Rates/Dynamics/190?startDate=2016-6-1&endDate=2016-6-30
# https://belgazprombank.by/export_courses.php
# skyscanner api, ryanair -api, билеты до 50 долларов по интересующим направлениям в интересующие даты
# cкармливаешь место, диапозон дат, получаешь,маршрут,цена,  компания, дата-время
# http://www.nbrb.by/apihelp/exrates
