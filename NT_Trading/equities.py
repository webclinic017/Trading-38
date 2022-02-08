from standards import moveMouse, leftClick, firstFind
import cv2
import numpy as np

class equity:
    class position:
        side = None
        profit = False
        loss = False
        previous = None
        entry = "Manual"
        wins = 0
        losses = 0

    def __init__(self, frame, x, y):
        self.position = equity.position()
        self.entryTimeTrigger = 0
        self.exitTimeTrigger = 0
        self.previousTick = 0
        self.strengthScore = 0
        self.x = x
        self.y = y
        self.w = 340
        self.h = 650
        self.tickArea = 0
        self.frame = frame[self.y:self.y + self.h, self.x:self.x + self.w]
        self.buyMkt = None
        self.sellMkt = None
        self.buyMktImg = cv2.imread('BuyMkt.png')
        self.sellMktImg = cv2.imread('SellMkt.png')
        self.buyMkt = firstFind(self.frame, self.buyMkt, self.buyMktImg)
        self.buyMkt = (self.buyMkt[0] + int(self.x) + 70, self.buyMkt[1] + int(self.y) + 395)
        if self.buyMkt:
            self.positionArearect = (int(self.buyMkt[0]) - 10, int(self.buyMkt[1]) - 55)
            self.profitLossArearect = (int(self.buyMkt[0]) + 10, int(self.buyMkt[1]) - 36)
            self.cancelExit = (self.buyMkt[0] + 160, self.buyMkt[1] - 31)
            self.tickStrikeArearect = (int(self.cancelExit[0]) - 120, int(self.cancelExit[1]) - 300)
        self.sellMkt = firstFind(self.frame, self.sellMkt, self.sellMktImg)
        self.sellMkt = (self.sellMkt[0] + int(self.x) - 160, self.sellMkt[1] + int(self.y) + 430)

    def universalExit(self):
        if self.position.loss:  # only if position is in loss already
            if self.position.side == "Long" and self.tickArea < 0:
                # close any long positions, order flow is down
                equity.close(self)
            elif self.position.side == "Short" and self.tickArea > 0:
                # close and short positions, order flow is up
                equity.close(self)

    def drawAreas(self, frame):
        cv2.circle(frame, (int(self.sellMkt[0]), int(self.sellMkt[1])), 5, (0, 255, 255), 15)
        cv2.circle(frame, (int(self.buyMkt[0]), int(self.buyMkt[1])), 5, (0, 255, 255), 15)
        cv2.circle(frame, (int(self.cancelExit[0]), int(self.cancelExit[1])), 5, (0, 255, 255), 15)
        cv2.rectangle(frame, (self.positionArearect[0]-5, self.positionArearect[1]-4), (self.positionArearect[0]+50, self.positionArearect[1]+4), (0, 255, 255), 2)
        cv2.rectangle(frame, (self.profitLossArearect[0]-1, self.profitLossArearect[1]-4), (self.profitLossArearect[0]+60, self.profitLossArearect[1]+4), (0, 255, 255), 2)
        cv2.rectangle(frame, (self.tickStrikeArearect[0] - 2, self.tickStrikeArearect[1] - 40), (self.tickStrikeArearect[0] + 2, self.tickStrikeArearect[1] + 70), (0, 255, 255), 2)
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (0, 255, 255), 2)
        cv2.putText(frame, "PrevTick: " + str(self.previousTick), (10 + self.x, (self.h-40) + self.y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (199, 0, 199), 3, cv2.LINE_AA)
        cv2.putText(frame, "Tick: " + str(self.tickArea), (10 + self.x, (self.h - 75) + self.y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (199, 0, 199), 3, cv2.LINE_AA)

    def getPosition(self, frame):
        self.entryTimeTrigger += 1
        self.exitTimeTrigger += 1
        # Checking position side
        self.positionArea = frame[self.positionArearect[1] - 4:self.positionArearect[1] + 4, self.positionArearect[0] - 5:self.positionArearect[0] + 50]
        greenPixels = np.argwhere(cv2.inRange(self.positionArea, (0, 140, 0), (100, 255, 100)))
        redPixels = np.argwhere(cv2.inRange(self.positionArea, (0, 0, 180), (100, 100, 255)))
        if redPixels.size >= 1:
            self.position.side = "Short"
            self.position.previous = "Short"
        elif greenPixels.size >= 1:
            self.position.side = "Long"
            self.position.previous = "Long"
        else:
            if self.entryTimeTrigger >= 90 and self.position.entry == "Auto":
                self.position.entry = "Manual"
            if self.position.side == self.position.previous:
                if self.position.profit:
                    self.position.wins += 1
                if self.position.loss:
                    self.position.losses += 1
            self.position.side = None
        # Checking position Profit or loss
        self.profitLossArea = frame[self.profitLossArearect[1] - 4:self.profitLossArearect[1] + 4, self.profitLossArearect[0] - 1:self.profitLossArearect[0] + 60]
        greenPixels = np.argwhere(cv2.inRange(self.profitLossArea, (0, 140, 0), (100, 255, 100)))
        redPixels = np.argwhere(cv2.inRange(self.profitLossArea, (0, 0, 200), (100, 100, 255)))
        self.position.profit = False
        self.position.loss = False
        if redPixels.size >= 1:
            self.position.loss = True
        elif greenPixels.size >= 1:
            self.position.profit = True
        cv2.putText(frame, "Position: " + str(self.position.side), (10 + self.x, (self.h-120) + self.y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (199, 0, 199), 3, cv2.LINE_AA)
        if self.position.side:
            cv2.putText(frame, str(self.position.entry), (10 + self.x, (self.h-190) + self.y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (199, 0, 199), 3, cv2.LINE_AA)
            if self.position.profit:
                cv2.putText(frame, "Profitable", (10 + self.x, (self.h-5) + self.y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (199, 0, 199), 3, cv2.LINE_AA)
            elif self.position.loss:
                cv2.putText(frame, "Losing", (10 + self.x, (self.h-5) + self.y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (199, 0, 199), 3, cv2.LINE_AA)
        else:
            cv2.putText(frame, "PrevPos: " + str(self.position.previous), (10 + self.x, (self.h-5) + self.y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (199, 0, 199), 3, cv2.LINE_AA)
        # Check tick striker area for up or down tick
        self.tickStrikeArea = frame[self.tickStrikeArearect[1] - 40:self.tickStrikeArearect[1] + 70, self.tickStrikeArearect[0] - 2:self.tickStrikeArearect[0] + 2]
        greenPixels = np.argwhere(cv2.inRange(self.tickStrikeArea, (0, 250, 0), (10, 255, 10)))
        redPixels = np.argwhere(cv2.inRange(self.tickStrikeArea, (0, 0, 250), (10, 10, 255)))
        if redPixels.size >= 1:
            #if self.tickArea != -(redPixels.size) and self.tickArea != 0:
                #self.previousTick = self.tickArea
            self.tickArea = -(redPixels.size)
        elif greenPixels.size >= 1:
            #if self.tickArea != greenPixels.size and self.tickArea != 0:
                #self.previousTick = self.tickArea
            self.tickArea = greenPixels.size
        elif self.tickArea != 0: #no ticks but tick is still set to != 0
            if self.previousTick != self.tickArea:
                self.previousTick = self.tickArea
            self.tickArea = 0
        cv2.putText(frame, "Strength: " + str(int(self.strengthScore/1000)), (10 + self.x, (self.h-160) + self.y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (199, 0, 199), 3, cv2.LINE_AA)
        equity.universalExit(self)

        #output wins and losses
        cv2.putText(frame, "W: " + str(self.position.wins), (10 + self.x, (self.h - 340) + self.y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (199, 0, 199), 3, cv2.LINE_AA)
        cv2.putText(frame, "L: " + str(self.position.losses), (10 + self.x, (self.h - 300) + self.y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (199, 0, 199), 3, cv2.LINE_AA)


    def enter(self, side):
        if self.entryTimeTrigger >= 90:
            self.position.entry = "Auto"
            moveMouse(side)
            leftClick()
            self.entryTimeTrigger = 0
            if side == self.buyMkt:
                print("Entered Long")
            elif side == self.sellMkt:
                print("Entered Short")

    def close(self):
        if self.exitTimeTrigger >= 20:
            moveMouse(self.cancelExit)
            leftClick()
            self.exitTimeTrigger = 0
            print("Position Closed")

    def tickStrategy(self, frame, strategyRunSession, currentSession, strengthCap, buff, manualTrigger):
        #cv2.putText(frame, str(self.entries), (10 + self.x, (self.h - 440) + self.y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (199, 0, 199), 3, cv2.LINE_AA)
        tradingTime = False
        if currentSession == strategyRunSession or manualTrigger:
            tradingTime = True  # only enter new positions during trading times, but close at any time
        cv2.putText(frame, "Trading: " + str(tradingTime), (100, 850), cv2.FONT_HERSHEY_SIMPLEX, 1.9, (199, 255, 0), 3, cv2.LINE_AA)
        if self.tickArea > 0:  # long trigger
            if self.position.profit and self.strengthScore < strengthCap:
                self.strengthScore += (self.tickArea * 0.5) * buff
            if self.position.side == "Short":  # Short position open, close it
                self.strengthScore = 0
                equity.close(self)
            if tradingTime:  # no position open but previous was short
                if self.position.previous != "Long":
                    equity.enter(self, self.buyMkt)
        elif self.tickArea < 0:  # short trigger
            if self.position.profit and self.strengthScore < strengthCap:
                self.strengthScore -= (self.tickArea * 0.5) * buff
            if self.position.side == "Long":  # Long position open, close it
                self.strengthScore = 0
                equity.close(self)
            if tradingTime:  # no position open and previous was long
                if self.position.previous != "Short":
                    equity.enter(self, self.sellMkt)
        else:  # no tick is found
            if self.position.loss and self.strengthScore <= 0 and self.position.entry == "Auto":
                equity.close(self)
        # in all scenarios, decay strength score
        if self.strengthScore > 0:
            if self.position.loss:
                self.strengthScore -= 20
            else:
                self.strengthScore -= 12

    def process(self, frame, strength):
        equity.drawAreas(self, frame)
        equity.getPosition(self, frame)
        strength += self.tickArea / 10
        return strength

    def reset(self):
        self.previousTick = 0
        self.position.previous = None
