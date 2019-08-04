from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class keyboard:
    def __init__(self, watcher, periodic, Timelist):
        self.watcher = watcher
        self.periodic = periodic
        self.timelist = Timelist
        self.make_photo = InlineKeyboardButton('make photo', callback_data='make_photo')
        self.periodic_photo = InlineKeyboardButton(self.periodic.button, callback_data='periodic_photo')
        self.watcher_settings = InlineKeyboardButton(self.watcher.button, callback_data='switch_watcher')
        self.timekeyboard =[]
        for item in Timelist:
            self.timekeyboard.append(InlineKeyboardButton(item,callback_data=item))
        self.main_keyboard = InlineKeyboardMarkup()
        self.main_keyboard.row(self.make_photo, self.periodic_photo, self.watcher_settings)
        self.main_keyboard.row(*self.timekeyboard[0:4])
        self.main_keyboard.row(*self.timekeyboard[4:8])
        self.main_keyboard.row(*self.timekeyboard[8:12])

    def update(self):
        self.__init__(self.watcher, self.periodic,self.timelist)