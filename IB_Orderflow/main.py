#  m6o77olf5

import time
from datetime import datetime
from IBpipeline import IBpipeline


def TimestampMillisec64():
	return int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)


if __name__ == "__main__":

    pipeline = IBpipeline()
    ES = pipeline.addContract("ESU2")
    ES1min = ES.addNewDelta(60)

    pipeline.requestMktData()

    switch = True
    while True:
        startFrameTime = TimestampMillisec64()



        candleClosed, delta, min, max, volume = ES1min.getDelta()
        if candleClosed:
            print("Delta:", delta, "Volume:", volume)
            print("Min:", min, "Max:", max)

        pipeline.receive()



        endFrameTime = TimestampMillisec64()
        RUNTIME = endFrameTime - startFrameTime

