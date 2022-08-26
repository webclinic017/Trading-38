import os
import queue

from ibapi.client import EClient
from ibapi.wrapper import EWrapper


class IBapi(EWrapper, EClient):
    pipe = queue.Queue()
    bidPrice = 0
    askPrice = 1

    def __init__(self):
        EClient.__init__(self, self)

    def tickSize(self, reqId, tickType, size):
        if tickType == 86:
            data = reqId, "openInterest", size
            self.pipe.put(data)

    def tickPrice(self, reqId , tickType, price:float, attrib):
        if tickType == 1:
            self.bidPrice = price
            data = reqId, "bidPrice", price
            self.pipe.put(data)
        elif tickType == 2:
            self.askPrice = price
            data = reqId, "askPrice", price
            self.pipe.put(data)
        pass

    def tickGeneric(self, reqId, tickType, value:float):
        pass

    def tickString(self, reqId, tickType, value:str):
        if tickType == 48:
            data = value.split(";")
            price = float(data[0])
            size = int(data[1].split(".")[0])
            time = data[2]
            daysVolume = data[3]
            vwap = data[4]

            data = reqId, time, price, size
            self.pipe.put(data)

        pass

