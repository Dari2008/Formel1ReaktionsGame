class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def getR(self) -> int:
        return self.r

    def getG(self) -> int:
        return self.g

    def getB(self) -> int:
        return self.b

    def setR(self, r):
        self.r = r

    def setG(self, g):
        self.g = g

    def setB(self, b):
        self.b = b

    def setBrightness(self, brightness):
        return Color(self.r * brightness, self.g * brightness, self.b * brightness)
    
    def getBrighness(self) -> int:
        return (self.r + self.g + self.b) / 3