import Color
from Color import Color
from rpi_ws281x import PixelStrip
from rpi_ws281x import Color as PixelColor

class Strip:
    def __init__(self, pin, length):
        self.length = length
        self.pixels = []
        self.strip = PixelStrip(length, pin, 800000, 10, False, 100, 0, ws.WS2812_STRIP)
        self.strip.begin()
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
        for i in range(self.length):
            self.strip.setPixelColor(i, PixelColor(self.pixels[i].getRed(), self.pixels[i].getGreen(), self.pixels[i].getBlue()))
        self.strip.show()
        pass

    def clear(self):
        for i in range(self.length):
            self.pixels[i] = Color(0, 0, 0)

    def getLength(self) -> int:
        return self.length