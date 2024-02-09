import Color
from Color import Color

class Strip:
    def __init__(self, pin, length):
        self.length = length
        self.pixels = []
        for i in range(length):
            self.pixels.append(Color(0, 0, 0))
        self.pin = pin

    def setPixel(self, pos, value):
        self.pixels[pos] = value

    def getPixel(self, pos) -> Color:
        return self.pixels[pos]

    def setPixels(self, index, color):
        if type(color) is not Color:
            return
        if type(index) is not int:
            return
        if index < 0 or index >= self.length:
            return
        self.pixels[index] = color
    
    def show(self):
        pass

    def clear(self):
        for i in range(self.length):
            self.pixels[i] = Color(0, 0, 0)

    def getLength(self) -> int:
        return self.length