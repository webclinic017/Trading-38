from datetime import datetime
import numpy as np
import cv2
import time
import ctypes

def firstFind(frame, obj, img):
	if obj is None:
		#src = [0,0, img.shape[1],img.shape[0]]
		match, x, y = findTemplate(img, frame)
		if match:
			object = (int(x), int(y))
			return object

def findTemplate(temp, frame):
	w = int(temp.shape[1] / 2)
	h = int(temp.shape[0] / 2)
	result = cv2.matchTemplate(frame, temp, cv2.TM_CCOEFF_NORMED)
	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)
	if maxVal >= .75:
		(startX, startY) = maxLoc
		endX = startX + temp.shape[1]
		endY = startY + temp.shape[0]
		return True, startX + w, startY + h
	else:
		return False, 0, 0

def checkStopHit(frame, lossLimit):
	if lossLimit: #if loss limit area is found, watch for loss limit to be hit
		lossLimitArea = (int(lossLimit[0]) + 90, int(lossLimit[1]))
		lossLimitArea = frame[lossLimitArea[1]-1:lossLimitArea[1]+5, lossLimitArea[0]:lossLimitArea[0]+2]
		loss = np.sum(lossLimitArea)
		cv2.line(lossLimitArea, (0, 0), (0, 50), (0, 255, 255), 2)
		if loss > 2000:
			return lossLimit, True
	else:
		lossLimit = firstFind(frame, lossLimit, cv2.imread('lossLimit.png'))
	return lossLimit, False

def getSession():
	now = datetime.now()
	euro = now.replace(hour=1, minute=0, second=0, microsecond=0)
	open = now.replace(hour=7, minute=30, second=0, microsecond=0)
	morning = now.replace(hour=8, minute=20, second=0, microsecond=0)
	slow = now.replace(hour=10, minute=00, second=0, microsecond=0)
	powerHour = now.replace(hour=13, minute=40, second=0, microsecond=0)
	eod = now.replace(hour=14, minute=2, second=0, microsecond=0)
	if now >= powerHour and now <= eod:
		#self.lossLimitMod = 96
		return "Power 20"
	elif now >= eod or now <= euro:
		return "ETH"
	elif now >= slow:
		#self.lossLimitMod = 96
		return "Slow"
	elif now >= morning:
		#self.lossLimitMod = 64
		return "Morning"
	elif now >= open:
		#self.lossLimitMod = 32
		return "Open"
	elif now >= euro:
		return "Euro"

def showFrame(frame):
	cv2.imshow('screen', frame)
	cv2.waitKey(1)

def moveMouse(loc):
	ctypes.windll.user32.SetCursorPos(int((5320 + loc[0])*1.5), int((825 + loc[1])*1.5)) #multiply by 1.5 for proper scaled location

def leftClick():
	ctypes.windll.user32.mouse_event(2, 0, 0, 0,0) # left down
	time.sleep(0.0001)
	ctypes.windll.user32.mouse_event(4, 0, 0, 0,0) # left up