from datetime import datetime
# business days - pandas??
# timezones! check in raspberry
class Today(datetime):
    def __init__(self):
        pass

    def get_current_datetime(self):
        self.today = datetime.date.today()
        self.weekno = today.weekday()
        self.now = datetime.datetime.now()

def time_in_range():
    start = datetime.time(8, 0, 0)
    end = datetime.time(10, 0, 0)
    start = datetime.datetime.combine(today, start)
    end = datetime.datetime.combine(today, end)
    if end <= start:
        end += datetime.timedelta(1) # tomorrow!
    if currenttime <= start:
        currenttime += datetime.timedelta(1) # tomorrow!
    return start <= currenttime <= end

if weekn o <5:
    isBusinessday = True
else:
    isBusinessday = False