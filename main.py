from GameThread import GameThread
import signal
import atexit
from Server import Server

class main:

    def __init__(self):
        self.currentPos = 0
        self.curves = [30, 65, 85, 109, 134, 164, 194, 234, 264, 284, 295]
        self.server = Server(5000)
        self.gameThread = GameThread(self.getCurves, self.server)
        Server.startNewGame = self.gameThread.start
        self.server.start()

    def getCurves(self):
        return self.curves
    

if __name__ == "__main__":
    main()