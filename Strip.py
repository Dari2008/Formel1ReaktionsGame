import Color
from Color import Color
import os
from Server import Server
if os.name != "nt":
    from rpi_ws281x import PixelStrip, ws
    from rpi_ws281x import Color as PixelColor

class Strip:
    def __init__(self, pin, length):
        self.length = length
        self.pixels = []
        if os.name != "nt":
            self.strip = PixelStrip(length, pin, 800000, 10, False, Server.BRIGHTESS, 0, ws.WS2812_STRIP)
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
        if os.name != "nt":
            for i in range(self.length):
                self.strip.setPixelColor(i, PixelColor(self.pixels[i].getR(), self.pixels[i].getG(), self.pixels[i].getB()))
            self.strip.show()
        else:
            # print("Showing")
            pass

    def clear(self):
        for i in range(self.length):
            self.pixels[i] = Color(0, 0, 0)

    def clearAndShow(self):
        self.clear()
        self.show()

    def getLength(self) -> int:
        return self.length