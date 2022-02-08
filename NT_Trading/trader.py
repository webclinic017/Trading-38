import numpy
import numpy as np
import time
import keyboard
import cv2
import cython
import standards
from standards import checkStopHit, getSession
import equities
import pyautogui
import mss.windows
mss.windows.CAPTUREBLT = 0
from mss import mss

display = {'top': 825, 'left': 5320, 'width': 1030, 'height': 900}
sct = mss()
fps = np.array([1,2,3,4,5])
marketStrength = 0
manualTrigger = False

def run(es, nq, rty, markets, lossLimit, FRAME):
    global manualTrigger
    global marketStrength
    global fps
    lastFrameTime = time.time()
    frame = cv2.cvtColor(np.array(sct.grab(display)), cv2.COLOR_BGRA2BGR)

    session = getSession()

    #check for stop loss hit
    lossLimit, stopHit = checkStopHit(frame, lossLimit)
    if stopHit or keyboard.is_pressed('0'):
        cv2.putText(frame, "STOP HIT", (150, 820), cv2.FONT_HERSHEY_SIMPLEX, 10.0, (255, 255, 255), 40, cv2.LINE_AA)
        for market in markets:
            if market.position.side is not None or keyboard.is_pressed('0'):  # A position is open while daily stop is hit, close it
                market.close()

    #create market objects
    if FRAME == 0:
        print("Creating market objects")
        es = equities.equity(frame, 0, 50)
        nq = equities.equity(frame, 340, 50)
        rty = equities.equity(frame, 680, 50)
        markets = [es, nq, rty]
        print("Market objects added to markets array")
        print("Starting Loop")
    else:
        for market in markets: #get all info on each market
            marketStrength = market.process(frame, marketStrength)

        if keyboard.is_pressed('up'):
            for market in markets:
                market.reset()
            manualTrigger = True
        elif keyboard.is_pressed('down'):
            manualTrigger = False

        #run desired strategies
        #At the open strategies
        if session == "Open":
            es.tickStrategy(frame, "Open", session, 6000, 1, False)
            nq.tickStrategy(frame, "Open", session, 6000, 1, False)
        else:
            #manually triggered strategies
            es.tickStrategy(frame, "None", session, 10000, 1, manualTrigger)
            nq.tickStrategy(frame, "None", session, 10000, 1, manualTrigger)
            #rty.tickStrategy(frame, "None", session, 10000, 1, manualTrigger)


    #frame cleanup
    if FRAME % 10800 == 0:  # keep pc awake
        pyautogui.press('shift')

    if FRAME % 30 == 0:
        fps[: -1] = fps[1:]; fps[-1] = (1 / (time.time() - lastFrameTime))
    avg = numpy.average(fps)

    cv2.putText(frame, str(int(avg)), (10, 845), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (199, 0, 199), 3, cv2.LINE_AA)
    cv2.putText(frame, session, (10, 895), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (199, 0, 199), 3, cv2.LINE_AA)
    cv2.putText(frame, "Market Strength: " + str(int(marketStrength)), (200, 895), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (199, 0, 199), 3, cv2.LINE_AA)

    standards.showFrame(frame)

    FRAME += 1

    return es, nq, rty, markets, lossLimit, FRAME