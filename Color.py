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

    def setBrightnessZeroToTwoFiveFive(self, brightness):
        return Color(round(max(0, min(255, self.r * brightness * 255))), round(max(0, min(255, self.g * brightness * 255))), round(max(0, min(255, self.b * brightness * 255))))
    
    def setBrightnessZeroToOne(self, brightness):
        return Color(round(max(0, min(1, self.r * brightness))), round(max(0, min(1, self.g * brightness))), round(max(0, min(1, self.b * brightness))))
    
    def getBrighness(self) -> int:
        return (self.r + self.g + self.b) / 3
    
    def __str__(self) -> str:
        return "R: " + str(self.r) + " G: " + str(self.g) + " B: " + str(self.b) + " Brightness: " + str(self.getBrighness())