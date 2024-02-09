from GameThread import GameThread
import signal
import atexit
from Server import Server

class main:

    def __init__(self):
        self.currentPos = 0
        self.curves = [30, 60, 90, 120, 150, 180, 210, 240, 270, 300]
        self.server = Server(5000)
        self.gameThread = GameThread(self.getCurves, self.server)
        Server.startNewGame = self.gameThread.start
        self.server.start()

    def getCurves(self):
        return self.curves
    

if __name__ == "__main__":
    main()