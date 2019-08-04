from datetime import time, date, datetime

class Today:
    def __init__(self,config):
        self.timebegin = time(config['begin'], 0, 0)
        self.timeend = time(config['end'], 0, 0)

    def Isbusinessday(self):
        return date.today().weekday() < 5

    def Isworktime(self):
        self.begin = datetime.combine(date.today(), self.timebegin)
        self.end = datetime.combine(date.today(), self.timeend)
        return self.begin <= datetime.now() <= self.end
  
