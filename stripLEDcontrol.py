import time, getopt, sys
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

PEGGY_PURPLE = Color(30,0,255)
HPS_LAMP = Color(255,70,0)

def SetSolid(color, strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(50/1000.0)

def SetSolidAll(color, strip_1, strip_2):
    for i in range(max(strip_1.numPixels(), strip_2.numPixels())):
        if i < max(strip_1.numPixels()):
            strip_1.setPixelColor(i, color)
        if i < max(strip_2.numPixels()):
            strip_2.setPixelColor(i, color)

def Blackout(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
        strip.show()

def main(options,args):
    strip_left = Adafruit_NeoPixel(LEFT_LED_COUNT, LEFT_LED_PIN, LEFT_LED_FREQ_HZ, LEFT_LED_DMA, LEFT_LED_INVERT, LEFT_LED_BRIGHTNESS, LEFT_LED_CHANNEL)
    strip_right = Adafruit_NeoPixel(RIGHT_LED_COUNT, RIGHT_LED_PIN, RIGHT_LED_FREQ_HZ, RIGHT_LED_DMA, RIGHT_LED_INVERT, RIGHT_LED_BRIGHTNESS, RIGHT_LED_CHANNEL)

    strip_left.begin()
    strip_right.begin()

    Blackout(strip_right)
    Blackout(strip_left)

    for opt, arg in options:
        if opt == '-s':
            arg_list = arg.split(',')
            vals = map(int, arg_list)
            SetSolid(Color(int(vals)), strip_right)
            SetSolid(Color(vals[0],vals[1],vals[2]), strip_left)
        if opt == '-a':
            vals = arg.split(',')
            SetSolidAll(Color(vals[0],vals[1],vals[2]), strip_right, strip_left)

    #SetSolid(HPS_LAMP, strip_right)
    #SetSolid(HPS_LAMP, strip_left)

    print('Press Ctrl-C to quit.')

if __name__ == '__main__':
    try:
        options, args = getopt.getopt(sys.argv[1:], "s:a:")
    except getopt.GetoptError:
        print('usage: stripLEDcontrol.py -s <hex color value>')
        sys.exit(2)
    main(options,args)