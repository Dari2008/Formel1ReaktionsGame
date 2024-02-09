from datetime import datetime
import json
import os

class Score:

    DATA = []
    screList = "./webpage/scores.json"

    if not os.path.exists(screList):
        with open(screList, "w") as file:
            file.write("[]")
            file.close()

    with open(screList, "r+") as file:
        DATA = json.load(file)
            
    @staticmethod
    def addScore(name: str, score: int, smallest: int):
        Score.DATA.append({"name": name, "smallest": smallest, "score": score, "time": datetime.now().strftime("%d.%m.%Y %H:%M")})
        with open(Score.screList, 'w') as file:
            json.dump(Score.DATA, file)

    @staticmethod
    def getScores(self):
        return self.data