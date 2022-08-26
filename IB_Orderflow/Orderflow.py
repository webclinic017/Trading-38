import os
from datetime import datetime
from constyle import Style, style, Attributes



os.system('color')
order = Style(Attributes.GREY, Attributes.BOLD)
buy = Style(Attributes.BRIGHT_GREEN, Attributes.BOLD)
sell = Style(Attributes.BRIGHT_RED, Attributes.BOLD)


class Orderflow:

    volume = 0
    buys = 0
    sells = 0

    deltas = []
    tickstrikes = []

    def __init__(self):
        pass

    def order(self, time, price, size):
        if size > 9 :
            print(order("ORDER  " + "{:.2f}".format(price) + "   " + str(size)))
        self.volume += size

    def buy(self, time, price, size):
        if size > 9:
            print(buy("BUY    " + "{:.2f}".format(price) + "   " + str(size)))
        self.volume += size
        self.buys += size

        for delta in self.deltas:
            delta.updateDelta(size)

    def sell(self, time, price, size):
        if size > 9:
            print(sell("SELL   " + "{:.2f}".format(price) + "   " + str(size)))
        self.volume += size
        self.sells += size

        for delta in self.deltas:
            delta.updateDelta(-size)

    def addNewDelta(self, interval):  # creates new delta time period to watch
        newDelta = Delta(interval)
        self.deltas.append(newDelta)
        return newDelta


class Delta:

    interval = 0
    delta = minDelta = maxDelta = volume = 0
    switch = False

    def __init__(self, interval):
        self.interval = interval  # store interval in seconds
        pass

    def updateDelta(self, size):
        if not self.volume:
            self.volume = abs(size)
            self.delta = size
            self.minDelta = self.delta
            self.maxDelta = self.delta
        else:
            self.volume += abs(size)
            self.delta += size
            if self.delta < self.minDelta:
                self.minDelta = self.delta
            if self.delta > self.maxDelta:
                self.maxDelta = self.delta


    def getDelta(self):
        nowSeconds = int(datetime.now().strftime("%S"))
        nowMinutes = int(datetime.now().strftime("%M"))

        intervalSeconds = self.interval if self.interval != 60 else 0
        intervalMinutes = self.interval / 60 if self.interval >= 60 else 0

        if self.interval <= 60:
            if intervalSeconds == nowSeconds:
                if self.switch:
                    self.switch = False
                    d = self.delta
                    min = self.minDelta
                    max = self.maxDelta
                    v = self.volume
                    self.reset()
                    return True, d, min, max, v
            else:
                self.switch = True
        else:
            if (intervalMinutes % nowMinutes == 0 or nowMinutes == 0) and nowSeconds == 0:
                if self.switch:
                    self.switch = False
                    d = self.delta
                    min = self.minDelta
                    max = self.maxDelta
                    v = self.volume
                    self.reset()
                    return True, d, min, max, v
            else:
                self.switch = True

        return False, self.delta, self.minDelta, self.maxDelta, self.volume


    def reset(self):
        volume = 0
        self.delta = self.minDelta = self.maxDelta = self.volume = 0


class Tickstrike:

    def __init__(self):
        pass







