import threading
from Server import Server
import math
import time
from Strip import Strip
from copy import copy
import json
import os
from Score import Score
import sys
if os.name == "nt":
    import keyboard

class GameThread:
    def __init__(self, getCurves, server):
        self.getCurves = getCurves
        self.currentPos = 0
        self.gameStop = False
        self.lastTime = time.time()
        self.deltaTime = 0
        self.currentBlinkTime = Server.BLINK_TIME
        self.isBlinkingOn = True
        self.isMoving = True
        self.waitingForInput = False
        self.passedCurves = copy(getCurves())
        self.times = []
        self.penaltys = []
        self.startTime = None
        self.gameStartTime = None
        self.gameRunning = True
        self.server: Server = server
        self.curveIndex = 0

        self.strip = Strip(18, 192) # länge: KP

        if os.name == "nt":
            keyboard.on_press_key("space", self.input)

    def start(self):
        self.gameStop = True

        while self.gameStop:
            time.sleep(0.3)

        #Reseting values
        self.isMoving = True
        self.waitingForInput = False
        self.passedCurves = copy(self.getCurves())
        self.times = []
        self.penaltys = []
        self.startTime = time.time()
        self.gameStartTime = time.time()
        self.gameStop = False
        self.lastTime = time.time()
        self.deltaTime = 0
        self.currentBlinkTime = Server.BLINK_TIME
        self.isBlinkingOn = True
        self.currentPos = 0
        self.curveIndex = 0

        #Starting game
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def clear(self):
        for i in range(self.strip.numpixels()):
            self.strip.setPixelColor(i, PixelColor(0, 0, 0))

    def stop(self):
        self.gameStop = True

    def run(self):
        print("Started GameThread")
        try:
            while not self.gameStop:
                self.deltaTime = time.time() - self.lastTime
                self.deltaTime = self.deltaTime if self.deltaTime != 0 else 0.0001
                self.lastTime = time.time()
                self.fps = 1 / self.deltaTime
                self.deltaTime = self.deltaTime * 10

                self.update()
                self.render()
                time.sleep(0.01)
        except KeyboardInterrupt:
            pass
        
        self.processDataAndSendToServer()

    def processDataAndSendToServer(self):
        timeTaken = 0
        reactionTimeTotal = 0
        penaltyTime = 0
        penaltyCount = 0
        smallest = sys.maxsize
        for timeData in self.times:
            reactionTimeTotal += timeData.get( "time")

        for penalty in self.penaltys:
            penaltyTime += penalty.get("time")
            penaltyCount += 1
        
        overallTimes = {}
        for timeData in self.times:
            overallTimes[timeData.get("curve")] = timeData.get("time")
            
        for penalty in self.penaltys:
            if overallTimes.__contains__(penalty.get("curve")):
                overallTimes[penalty.get("curve")] += penalty.get("time")

    
        for timeData in overallTimes:
            if overallTimes.get(timeData) < smallest:
                smallest = overallTimes.get(timeData)

        reactionTimeTotal = (reactionTimeTotal).__round__(2)
        timeTaken = ((reactionTimeTotal + penaltyTime)).__round__(2)
        penaltyTime = (penaltyTime).__round__(2)
        reactionTimeAvg = (reactionTimeTotal / len(self.times)).__round__(2)


        print("Time taken: " + str(timeTaken))
        print("Reaction time total: " + str(reactionTimeTotal))
        print("Reaction time avg: " + str(reactionTimeAvg))
        print("Penalty time: " + str(penaltyTime))
        print("Penalty count: " + str(penaltyCount))
        print("Times: " + str(self.times))

        place = 1

        for score in Score.DATA:
            if score.get("score") < smallest:
                place += 1

        print(place)

        self.server.update(timeTaken, reactionTimeAvg, penaltyTime, penaltyCount, self.times, self.penaltys, place, reactionTimeAvg, smallest)
        Score.addScore(Server.NAME, reactionTimeAvg, smallest)

        pass

                
    def getDeltaTime(self):
        return self.deltaTime

                
    def render(self):
        self.strip.clear()
        for i in range(math.floor(self.currentPos)):
            self.strip.setPixels(i, Server.CURRENT_POISITION_COLOR)

        self.strip.setPixels(math.floor(self.currentPos)+1, Server.CURVE_COLOR.setBrightness(self.currentPos/1))
        
        if self.isBlinkingOn and self.getNextCurve() != None and self.getNextCurve() < self.strip.getLength():
                self.strip.setPixels(self.getNextCurve(), Server.CURVE_COLOR)

        self.strip.show()

        self.printStrip()

    def input(self, e):
        if(self.gameStop):
            self.gameStop = False
            return
        if self.waitingForInput:
            if self.startTime != None:
                self.isMoving = True
                self.waitingForInput = False
                self.times.append({"time": ((time.time() - self.startTime)*1000).__round__(2), "curve": self.curveIndex})
                self.startTime = None
        else:
            self.penaltys.append({"time": Server.PENALTY_TIME_MS, "curve": (self.curveIndex+1), "penalty": True, "reason": "Zu früh gedrückt"})

    def startPress(self):
        pass


    def stopPress(self):
        pass

    def printStrip(self):
        result = ""
        spacer = ""

        for i in range(self.strip.getLength()):
            if i == self.getNextCurve() and self.isBlinkingOn:
                result += "S" + spacer
            else:
                result += str("█" if self.strip.getPixel(i).getBrighness() == Server.CURRENT_POISITION_COLOR.getBrighness() else "S" if self.strip.getPixel(i).getBrighness() == Server.CURVE_COLOR.getBrighness() else " ") + spacer


        print(result)


    def getNextCurve(self):
        tmpCurves = self.getCurves()
        tmpCurves.sort()
        for curve in tmpCurves:
            if curve > self.currentPos:
                return curve


    def update(self):
        if self.currentPos >= self.strip.getLength():
            self.gameStop = True
            self.currentPos = 0
            print(f"Game ended")
            return
        
        if self.isMoving:
            self.currentPos += 1 * self.getDeltaTime()

        self.currentBlinkTime -= Server.SPEED * self.getDeltaTime()

        
        if self.getNextCurve() in self.passedCurves and self.currentPos+self.deltaTime >= self.getNextCurve():
            self.isMoving = False
            self.waitingForInput = True
            self.passedCurves.remove(self.getNextCurve())
            self.startTime = time.time()
            self.curveIndex += 1
        
        if self.currentBlinkTime <= 0:
            self.isBlinkingOn = not self.isBlinkingOn
            self.currentBlinkTime = Server.BLINK_TIME