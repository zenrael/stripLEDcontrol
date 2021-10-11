import time, argparse
from rpi_ws281x import *

# RIGHT HAND SIDE IS STRIP 1

RIGHT_LED_COUNT = 35
RIGHT_LED_PIN = 12
RIGHT_LED_FREQ_HZ = 800000
RIGHT_LED_DMA = 10
RIGHT_LED_BRIGHTNESS = 255
RIGHT_LED_INVERT = False
RIGHT_LED_CHANNEL = 0

LEFT_LED_COUNT = 48
LEFT_LED_PIN = 13 # 13 IS CHANNEL 1
LEFT_LED_FREQ_HZ = 800000
LEFT_LED_DMA = 10
LEFT_LED_BRIGHTNESS = 255
LEFT_LED_INVERT = False
LEFT_LED_CHANNEL = 1

PEGGY_PURPLE = (30,0,255)
HPS_LAMP = (255,70,0)

def SetSolid(color, strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(50/1000.0)

def Blackout(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
        strip.show()

if __name__ == '__main__':
    strip_left = Adafruit_NeoPixel(LEFT_LED_COUNT, LEFT_LED_PIN, LEFT_LED_FREQ_HZ, LEFT_LED_DMA, LEFT_LED_INVERT, LEFT_LED_BRIGHTNESS, LEFT_LED_CHANNEL)
    strip_right = Adafruit_NeoPixel(RIGHT_LED_COUNT, RIGHT_LED_PIN, RIGHT_LED_FREQ_HZ, RIGHT_LED_DMA, RIGHT_LED_INVERT, RIGHT_LED_BRIGHTNESS, RIGHT_LED_CHANNEL)

    strip_left.begin()
    strip_right.begin()

    Blackout(strip_right)
    SetSolid(Color(255,70,0), strip_right)

    print('Press Ctrl-C to quit.')
