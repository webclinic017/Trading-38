from IBapi import IBapi
import Contracts
import threading
import time


class IBpipeline():

    ib = IBapi()
    contracts = []

    def __init__(self):
        print("Creating Bot")

        self.ib.connect("127.0.0.1", 7496, 36)
        connect = threading.Thread(target=self.connect, daemon=True)
        connect.start()

    def addContract(self, symbol: str):
        newContract = Contracts.Future(len(self.contracts), symbol)
        self.contracts.append(newContract)
        return newContract

    def connect(self):
        print("Starting Connection Thread")
        self.ib.run()

    def requestMktData(self):
        time.sleep(1)
        print("Starting Bot")
        for contract in self.contracts:
            print("Requesting", contract.symbol, "Market Data with ID", contract.id)
            self.ib.reqMktData(contract.id, contract.IBcontractObject, "233,294,295,588", False, False, [])

    def receive(self):
        if not self.ib.pipe.empty():
            data = self.ib.pipe.get(block=True, timeout=0.1)
            contractID = data[0]
            self.contracts[contractID].pipe.put(data[1:])  # forward all data to the contract except the ID

        for contract in self.contracts:  # cycle receiving pipes for all contracts
            contract.receive()


