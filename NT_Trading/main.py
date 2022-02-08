import cython
import trader
import time

FRAME: cython.int
FRAME = 0

lossLimit = None

es = []
nq = []
rty = []
markets = []

while True:
    es, nq, rty, markets, lossLimit, FRAME = trader.run(es, nq, rty, markets, lossLimit, FRAME)
