from Color import Color
from http.server import SimpleHTTPRequestHandler
from http.server import HTTPServer
from Score import Score
from ssl import PROTOCOL_TLS_SERVER, SSLContext
import json
import os

class Server:
    CURRENT_POISITION_COLOR: Color = Color(0, 255, 0)
    CURVE_COLOR: Color = Color(216, 89, 26)
    BLINK_TIME: float = 0.1
    SPEED: float = 10  #pro sekunde
    PENALTY_TIME_MS: int = 300
    DIRECTORY = "./webpage/"
    CURRENT_RACE_DATA = "{}"
    LAST_CURRENT_RACE_DATA = "{}"
    NAME = ""
    PLACE = 0
    SCORE = 0
    MINIMAL = 0

    def defaultStartGame():
        pass


    startNewGame = defaultStartGame

    def __init__(self, port):
        super().__init__()
        self.port = port
        Server.CURRENT_RACE_DATA = json.dumps({})

    def update(self, timeTaken, reactionTimeAvg, penaltyTime, penaltyCount, times, penaltys, place, score, minimal):
        Server.SCORE = score
        Server.PLACE = place
        Server.MINIMAL = minimal
        Server.CURRENT_RACE_DATA = json.dumps(
            {"timeTaken": timeTaken, 
             "reactionTimeAvg": reactionTimeAvg, 
             "penaltyTime": penaltyTime, 
             "penaltyCount": penaltyCount, 
             "times": times, 
             "penaltys": penaltys, 
             "penaltyTimePerPenalty": Server.PENALTY_TIME_MS
            }
        )

    def get_ip(self):
        return self.ip

    def get_port(self):
        return self.port
    
    def start(self):
        ssl_context = SSLContext(PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain("./certificate/cert.pem", "./certificate/private.key")

        self.server = HTTPServer(("localhost", self.port), ServerHandler)
        
        self.server.socket = ssl_context.wrap_socket(self.server.socket, server_side=True)
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            pass

        self.server.server_close()

    @staticmethod
    def getResponse():
        return Server.CURRENT_RACE_DATA

    def __str__(self):
        return f"Server: {self.port}"

class ServerHandler(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=Server.DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == "/startGame":
            content_len = int(self.headers.get('content-length', 0))
            data = self.rfile.read(content_len).decode("utf-8")
            Server.NAME = data
            print(f"Starting game for {Server.NAME}...")
            Server.startNewGame()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            return


    def do_GET(self):
        if self.path == "/raceData.json":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(Server.getResponse(), "utf-8"))
            return

        if self.path == "/favicon.ico":
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            return
        elif self.path == "/isNewData.json":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            if Server.LAST_CURRENT_RACE_DATA == Server.CURRENT_RACE_DATA:
                self.wfile.write(bytes(json.dumps({"update": False}), "utf-8"))
            else:
                Server.LAST_CURRENT_RACE_DATA = Server.CURRENT_RACE_DATA
                self.wfile.write(bytes(json.dumps({"update": True, "place": Server.PLACE, "score": Server.SCORE, "minimal": Server.MINIMAL}), "utf-8"))
            return
        
        elif self.path == "/getScores.json":
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(Score.DATA), "utf-8"))
            return

        return super().do_GET()


if __name__ == "__main__":
    server = Server(5000)
    server.start()