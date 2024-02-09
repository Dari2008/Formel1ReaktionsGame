class Color:
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    def getR(self) -> int:
        return self.r

    def getG(self) -> int:
        return self.g

    def getB(self) -> int:
        return self.b

    def setR(self, r: int):
        self.r = r

    def setG(self, g: int):
        self.g = g

    def setB(self, b: int):
        self.b = b

    def setBrightness(self, brightness):
        return Color(self.r * brightness, self.g * brightness, self.b * brightness)
    
    def getBrighness(self) -> int:
        return (self.r + self.g + self.b) / 3