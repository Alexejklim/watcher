class watcher:
    def __init__(self):
        self.Isrun = True
        self.button = 'switch off watcher'

    def switch(self):
        if self.Isrun:
            self.Isrun = False
            self.button = 'switch on watcher'
            self.message = 'Watcher is stopped. Something else?'
        else:
            self.Isrun = True
            self.button = 'switch off watcher'
            self.message = 'Watcher is run. Something else?'

class periodic:
    def __init__(self):
        self.Isrun = False
        self.button = 'switch on periodic'
        self.period = 5

    def switch(self):
        if self.Isrun:
            self.Isrun = False
            self.button = 'switch on periodic'
            self.message = 'Periodic mailing is stopped. Something else?'
        else:
            self.Isrun = True
            self.button = 'switch off periodic'
            self.message = 'Periodic mailing is run. Something else?'

    def set_period(self,period):
        self.period = period
