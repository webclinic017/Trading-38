import queue
from datetime import datetime
from ibapi.contract import Contract
from Orderflow import Orderflow


class Future(Orderflow):

    symbol = None
    id = None
    IBcontractObject = None
    pipe = queue.Queue()
    delayQueue = queue.Queue()

    openInterest = 0
    bidPrice = 0
    askPrice = 0
    delayTimer = 0

    def __init__(self, id, symbol):
        self.id = id
        self.IBcontractObject = Contract()
        self.IBcontractObject.secType = "FUT"
        self.IBcontractObject.exchange = "GLOBEX"
        self.IBcontractObject.currency = "USD"
        self.IBcontractObject.localSymbol = self.symbol = symbol

    def receive(self):
        if not self.pipe.empty():
            data = self.pipe.get(block=True, timeout=0.1)

            if len(data) == 2:  # Open Interest and Bid/Ask
                self.delayQueue.put(data)

            if len(data) == 3:  # buy/sell prices and volumes, send to orderflow
                mstime = int(data[0])
                price = data[1]
                size = data[2]
                if price >= self.askPrice:
                    self.buy(mstime, price, size)
                elif price <= self.bidPrice:
                    self.sell(mstime, price, size)
                else:
                    self.order(mstime, price, size)
        else:
            if not self.delayQueue.empty():
                data = self.delayQueue.get(block=True, timeout=0.1)
                dataName = data[0]
                dataValue = data[1]
                self.__setattr__(dataName, dataValue)






def TimestampMillisec64():
	return int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)

